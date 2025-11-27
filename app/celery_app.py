from celery import Celery
from app.config import get_settings

settings = get_settings()

celery_app = Celery(
    "pdf_extraction",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
    include=["app.tasks.extraction"]
)

celery_app.conf.update(
    task_track_started=settings.celery_task_track_started,
    task_time_limit=settings.celery_task_time_limit,
    result_expires=settings.celery_result_expires,
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

if __name__ == "__main__":
    celery_app.start()
