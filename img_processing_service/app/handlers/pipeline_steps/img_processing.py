import asyncio
import imghdr

from celery.result import AsyncResult
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.datastructures import UploadFile

from app.db.session import get_async_session
from app.handlers.celery_worker.tasks import process_image
from app.handlers.pipeline_steps.base import (
    BasePipelineStepsHandler,
)
from app.models.pipeline_tasks import PipelineTask


class ImageProcessingHandler(BasePipelineStepsHandler):
    def __init__(
        self,
        input_data: UploadFile,
        pipeline_task: PipelineTask,
        session: AsyncSession = Depends(get_async_session),
    ):
        self.input_data = input_data
        self.pipeline_task = pipeline_task
        self.session = session

    async def process(
        self, *args, **kwargs
    ) -> tuple[bytes, PipelineTask, AsyncSession]:
        self.validate_input_data()
        image_bytes = await self.input_data.read()
        task_id = process_image.delay(image_bytes).id
        result = await self.execute_celery_task(task_id)
        return result, self.pipeline_task, self.session

    @staticmethod
    def is_valid_image_file(file: UploadFile) -> bool:
        file_type = imghdr.what(file.file)
        return file_type in ("jpg", "jpeg")

    def validate_input_data(self) -> None:
        if not isinstance(self.input_data, UploadFile):
            raise ValueError("Invalid input data type")
        if not self.is_valid_image_file(self.input_data):
            raise ValueError("Invalid image file - jpg or jpeg were expected")

    @staticmethod
    async def execute_celery_task(task_id: str) -> bytes:
        async_result = AsyncResult(task_id)
        while not async_result.ready():
            await asyncio.sleep(0.1)
        result = async_result.result
        async_result.forget()
        return result
