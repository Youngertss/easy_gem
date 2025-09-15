import os
from dotenv import load_dotenv
from celery import Celery

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
session_maker = sessionmaker(engine, expire_on_commit=False)

load_dotenv(".env")
CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND")

celery = Celery(
    "worker",
    broker = CELERY_BROKER_URL,
    backend = CELERY_RESULT_BACKEND
)

celery.autodiscover_tasks(['src.tasks'])
