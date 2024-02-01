from typing import Any

from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_async_session
from app.db_queries.pipeline_tasks import db_pipeline_tasks
from app.db_queries.pipelines import db_pipeline
from app.handlers.pipeline_handler import PipelineHandler
from app.handlers.registry import HandlersRegistry
from app.schemas.pipeline_task import PipelineTaskOut

router = APIRouter()


@router.post("/process-image", response_model=PipelineTaskOut)
async def process_image(
    pipeline_id: int,
    image_file: UploadFile,
    session: AsyncSession = Depends(get_async_session),
) -> Any:
    pipeline = await db_pipeline.get_pipeline(session, pipeline_id)
    if not pipeline:
        raise HTTPException(status_code=404, detail="Pipeline not found")
    pipeline_task = await db_pipeline_tasks.create_pipeline_task(
        session, pipeline.id, image_file.filename
    )
    try:
        steps_handlers = HandlersRegistry.get_handlers(pipeline.steps)
        pipeline_handler = PipelineHandler(
            steps_handlers, image_file, pipeline_task, session
        )
        pipeline_task = await pipeline_handler.process()
        return pipeline_task
    except ValueError as err:
        raise HTTPException(status_code=400, detail=f"{err}")


