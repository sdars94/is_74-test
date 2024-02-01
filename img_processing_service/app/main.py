from fastapi import FastAPI

from app.conf.settings import settings
from app.api.endpoints import router as api_router

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(api_router, prefix=settings.API_STR)


