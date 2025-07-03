from contextlib import asynccontextmanager

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.auth.auth import fastapi_users, auth_backend, current_user
from src.auth.schemas import UserRead, UserCreate, UserUpdate
from src.games.routers import router as games_router, users_update_router

# from src.auth.models import create_db_and_tables
# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # Not needed if you setup a migration system like Alembic
#     await create_db_and_tables()
#     yield

app = FastAPI()

#statisfiles
app.mount("/imgs", StaticFiles(directory="src/imgs"), name="imgs")

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:8080",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*", "/patch", "patch"],
    allow_headers=["*"],
)


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

# users/me - for frontend check
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)

app.include_router(games_router)
app.include_router(users_update_router)