from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models.pipelines import Pipeline
from .base import DBBase


class DBPipeline(DBBase[Pipeline]):
    async def get_pipeline(
        self, session: AsyncSession, pipeline_id: int
    ) -> Pipeline | None:
        pipeline = await session.get(
            self.model,
            pipeline_id,
            options=[joinedload(self.model.steps)],
        )
        return pipeline


db_pipeline = DBPipeline(Pipeline)
