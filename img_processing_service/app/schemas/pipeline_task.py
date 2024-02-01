from pydantic import BaseModel


class PipelineTaskOut(BaseModel):
    id: int
    pipeline_id: int
    status: str
    filename: str
    data: dict | list = []
