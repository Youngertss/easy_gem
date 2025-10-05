import os
from contextlib import asynccontextmanager

from fastapi.responses import FileResponse
from fastapi import APIRouter, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from src.auth.auth import auth_backend, current_user, fastapi_users
from src.auth.routers import additional_users_router
from src.auth.schemas import UserCreate, UserRead, UserUpdate
from src.chat.routers import router as chat_router
from src.games.routers import router as games_router
from src.statistics.routers import router as statistics_router
from src.bonuses.routers import bonuses_router
from src.tasks import test_task
from src.utils import InsufficientBalanceException


app = FastAPI()

@app.get("/api/health")
async def health():
    return {"status": "ok"}

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


@app.middleware("http")
async def balance_exception_middleware(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except InsufficientBalanceException as exc:
        return JSONResponse(
            status_code=400,
            content={
                "error": "Insufficient balance",
                "user_id": exc.user_id,
                "required": float(exc.required),
                "current": float(exc.current),
            },
        )
    except Exception as exc:
        return JSONResponse(status_code=500, content={"error": "Internal server error"})


@app.middleware("http")
async def spa_fallback(request, call_next):
    response = await call_next(request)
    if response.status_code == 404:     
        path = request.url.path
        if not path.startswith("/games") and not path.startswith("/imgs"):
            index_path = os.path.join("frontend", "build", "index.html")
            if os.path.exists(index_path):
                return FileResponse(index_path)
    return response


@app.get("/celery_test_endpoint")
async def celery_test_endpoint(t: int, res: str) -> dict:
    response = test_task.delay(t, res)
    ...
    return JSONResponse({"response": f"task creted"})


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

app.include_router(statistics_router)
app.include_router(chat_router)
app.include_router(games_router)
app.include_router(bonuses_router)


# statisfiles
app.mount("/imgs", StaticFiles(directory="src/imgs"), name="imgs")
app.mount("/", StaticFiles(directory="frontend/build", html=True), name="frontend")
