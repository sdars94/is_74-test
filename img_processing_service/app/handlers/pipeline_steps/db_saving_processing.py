from typing import Any

from fastapi import Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_async_session
from app.db_queries.pipeline_tasks import db_pipeline_tasks
from app.models.pipeline_tasks import PipelineTask
from .base import BasePipelineStepsHandler


class DBInputData(BaseModel):
    data: Any


class DBSavingHandler(BasePipelineStepsHandler):
    def __init__(
        self,
        input_data: type[DBInputData],
        pipeline_task: PipelineTask,
        session: AsyncSession = Depends(get_async_session),
    ) -> None:
        self.input_data = input_data
        self.pipeline_task = pipeline_task
        self.session = session

    async def process(
        self, *args, **kwargs
    ) -> tuple[Any, PipelineTask, AsyncSession]:
        self.validate_input_data()
        data = self.get_pipeline_task_info()
        self.pipeline_task = self.update_pipeline_task_data(data)
        self.pipeline_task = await self.update_pipeline_task_db()
        return data, self.pipeline_task, self.session

    async def update_pipeline_task_db(self) -> PipelineTask:
        pipeline_task = await db_pipeline_tasks.update_pipeline_task(
            self.session, self.pipeline_task
        )
        return pipeline_task

    def update_pipeline_task_data(
        self, data: BaseModel | list
    ) -> PipelineTask:
        if data:
            self.pipeline_task.status = "detected"
            self.pipeline_task.data = data.model_dump()
        else:
            self.pipeline_task.status = "undetected"
            self.pipeline_task.data = data
        return self.pipeline_task

    def get_pipeline_task_info(self) -> Any:
        return self.input_data.data

    def validate_input_data(self) -> None:
        if (
            not isinstance(self.input_data, BaseModel)
            or "data" not in self.input_data.model_dump()
        ):
            raise ValueError("Invalid input data type")
