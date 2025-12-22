from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routers import main_router

app = FastAPI(title="RAG Model")
app.include_router(main_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # или ["*"] для всех, но лучше явно
    allow_credentials=True,
    allow_methods=["*"],  # или перечисли нужные методы: ["GET", "POST", ...]
    allow_headers=["*"],  # или перечисли нужные заголовки
)
