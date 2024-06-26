from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.auth.auth import fastapi_users, auth_backend, current_user
from src.auth.schemas import UserRead, UserCreate
from src.auth.models import create_db_and_tables
from src.games.routers import router as games_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Not needed if you setup a migration system like Alembic
    await create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def initial():
    return {"message":"it works"}


app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(games_router)