import random
from typing import Any, Union

from fastapi import FastAPI, UploadFile
from pydantic import BaseModel

app = FastAPI(title="ML SERVICE")


class DataOut(BaseModel):
    top_left_x: int
    top_left_y: int
    width: int
    height: int
    confidence: float
    class_id: int


@app.post("/ml-process-img", response_model=Union[DataOut, list])
async def ml_img_process(image: UploadFile) -> Any:
    response_data = get_ml_response_data()
    return response_data


def get_ml_response_data():
    if random.choice([True, False]):
        image_width = 640
        image_height = 640
        top_left_x = random.randint(0, image_width - 300)
        top_left_y = random.randint(0, image_height - 300)
        width = random.randint(100, 300)
        height = random.randint(100, 300)
        confidence = random.uniform(0.7, 0.95)
        return DataOut(
            top_left_x=top_left_x,
            top_left_y=top_left_y,
            width=width,
            height=height,
            confidence=confidence,
            class_id=1,
        )
    else:
        return []
