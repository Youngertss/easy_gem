Site for gambling

backend start:
uvicorn src.main:app

frontend start:
npm start

alembic migrations:

alembic revision --autogenerate -m "..."
alembic upgrade head

