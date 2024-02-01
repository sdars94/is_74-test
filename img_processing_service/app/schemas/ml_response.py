from pydantic import BaseModel


class MLData(BaseModel):
    top_left_x: int
    top_left_y: int
    width: int
    height: int
    confidence: float
    class_id: int


class MLHandlerOut(BaseModel):
    data: MLData | list = []
