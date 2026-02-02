from celery import Celery

from app.core.config import settings

celery = Celery(
    "judicial",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

celery.conf.task_track_started = True
