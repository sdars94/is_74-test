from celery import Celery

from app.conf.settings import settings

celery = Celery(
    __name__,
    broker=str(settings.REDIS_URL),
    backend=str(settings.REDIS_URL),
)
# celery -A app.handlers.celery_worker.conf.celery flower
# celery -A app.handlers.celery_worker.tasks worker --loglevel=info --pool solo
