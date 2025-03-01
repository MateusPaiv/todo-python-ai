from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from app.api.user import router as user_router
from app.api.todo import router as todo_router

app = FastAPI(title="API For ToDo List", version="0.1.0")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(todo_router)
