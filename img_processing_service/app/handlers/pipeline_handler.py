from typing import Any
from collections import deque

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_async_session
from app.handlers.registry import HandlerType
from app.models.pipeline_tasks import PipelineTask


class PipelineHandler:
    def __init__(
        self,
        handlers: list[HandlerType],
        input_data: Any,
        pipeline_task: PipelineTask,
        session: AsyncSession = Depends(get_async_session),
    ) -> None:
        self.handlers = deque(handlers)
        self.data = input_data
        self.pipeline_task = pipeline_task
        self.session = session

    async def process(self) -> PipelineTask:
        while self.handlers:
            handler_class: type[HandlerType] = self.handlers.popleft()
            handler: HandlerType = handler_class(
                self.data, self.pipeline_task, self.session
            )
            (
                self.data,
                self.pipeline_task,
                self.session,
            ) = await handler.process()
        return self.pipeline_task
