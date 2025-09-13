import os
from dotenv import load_dotenv
from celery import Celery

load_dotenv(".env")

CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND")

celery = Celery(
    "worker",
    broker = CELERY_BROKER_URL,
    backend = CELERY_RESULT_BACKEND
)

celery.autodiscover_tasks(['src.tasks'])
