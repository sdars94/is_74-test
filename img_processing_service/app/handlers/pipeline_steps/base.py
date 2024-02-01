from abc import ABC, abstractmethod


class StepHandlerResource:
    def __init__(self, url: str):
        self.url = url


class BasePipelineStepsHandler(ABC):
    @abstractmethod
    def validate_input_data(self):
        ...

    @abstractmethod
    async def process(self, *args, **kwargs):
        ...
