"""Core Celery Configuration"""
from celery import Celery
from src.main import app_settings, app_logger

celery = Celery("src.main",\
    broker=app_settings.CELERY_BROKER_URL, \
    backend=app_settings.CELERY_RESULT_BACKEND, \
    include=['src.app.utils.celery_tasks.email_tasks'])
celery.conf.update(
    result_expires=3600,
    worker_heartbeat=120
)
app_logger.info("celery app created and configured")
