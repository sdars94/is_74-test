from typing import TypeVar

from app.models.pipelines import PipelineStep
from .pipeline_steps import (
    DBSavingHandler,
    ImageProcessingHandler,
    MLProcessingHandler,
)
from .pipeline_steps.base import BasePipelineStepsHandler

HandlerType = TypeVar("HandlerType", bound=BasePipelineStepsHandler)


class HandlersRegistry:
    handlers: dict[str, HandlerType] = {
        "ImageProcessorHandler": ImageProcessingHandler,
        "MLProcessorHandler": MLProcessingHandler,
        "DBSavingHandler": DBSavingHandler,
    }

    @classmethod
    def get_handlers(
        cls, pipeline_steps: list[PipelineStep]
    ) -> list[HandlerType]:
        if not all(step.handler in cls.handlers for step in pipeline_steps):
            raise ValueError("Unknown handler")
        return [cls.handlers[step.handler] for step in pipeline_steps]
