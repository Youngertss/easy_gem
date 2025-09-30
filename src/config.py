import os

from dotenv import load_dotenv

load_dotenv()
SECRET = os.environ.get("SECRET")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

REDIS_URL = os.environ.get("REDIS_URL")
DB_HOST_ALEMBIC = os.environ.get("DB_HOST_ALEMBIC")

CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND")

# SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD')
# SMTP_USER = os.environ.get('SMTP_USER')
