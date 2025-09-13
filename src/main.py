from contextlib import asynccontextmanager

from fastapi import FastAPI, APIRouter
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.auth.auth import fastapi_users, auth_backend, current_user
from src.auth.schemas import UserRead, UserCreate, UserUpdate
from src.games.routers import router as games_router
from src.chat.routers import router as chat_router
from src.auth.routers import additional_users_router

from src.tasks import test_task
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

@app.get("/celery_test_endpoint")
async def celery_test_endpoint(t: int, res: str) -> dict:
    response = test_task.delay(t, res)
    ...
    return JSONResponse({"response":f"task creted"})


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
app.include_router(additional_users_router)

app.include_router(chat_router)
app.include_router(games_router)