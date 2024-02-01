import httpx
from fastapi import Depends
from httpx import Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.conf.settings import settings
from app.db.session import get_async_session
from app.models.pipeline_tasks import PipelineTask
from app.schemas.ml_response import MLHandlerOut
from .base import BasePipelineStepsHandler


class MLProcessingHandler(BasePipelineStepsHandler):
    def __init__(
        self,
        input_data: bytes,
        pipeline_task: PipelineTask,
        session: AsyncSession = Depends(get_async_session),
    ) -> None:
        self.input_data = input_data
        self.resource_url = settings.ML_SERVICE_URL
        self.pipeline_task = pipeline_task
        self.session = session

    async def process(
        self, *args, **kwargs
    ) -> tuple[MLHandlerOut, PipelineTask, AsyncSession]:
        self.validate_input_data()
        ml_response = await self.get_ml_response()
        result = self.get_ml_response_data(ml_response)
        return result, self.pipeline_task, self.session

    @staticmethod
    def get_ml_response_data(response: Response) -> MLHandlerOut:
        data: dict = response.json()
        return MLHandlerOut(data=data) if data else MLHandlerOut()

    async def get_ml_response(self):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.resource_url,
                files={"image": ("image.jpg", self.input_data, "image/jpeg")},
            )
            return response

    def validate_input_data(self) -> None:
        if not isinstance(self.input_data, bytes):
            raise ValueError("Invalid input data type")
