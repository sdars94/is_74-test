from sqlalchemy.ext.asyncio import AsyncSession

from app.models.pipeline_tasks import PipelineTask
from .base import DBBase


class DBPipelineTask(DBBase[PipelineTask]):
    async def create_pipeline_task(
        self, session: AsyncSession, pipeline_id: int, file_name: str
    ) -> PipelineTask:
        pipeline_task = self.model(pipeline_id=pipeline_id, filename=file_name)
        session.add(pipeline_task)
        await session.commit()
        return pipeline_task

    @staticmethod
    async def update_pipeline_task(
        session: AsyncSession, pipeline_task: PipelineTask
    ) -> PipelineTask:
        session.add(pipeline_task)
        await session.commit()
        return pipeline_task


db_pipeline_tasks = DBPipelineTask(PipelineTask)
