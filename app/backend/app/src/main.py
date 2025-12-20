from fastapi import FastAPI

from src.routers import main_router

app = FastAPI(title="RAG Model")
app.include_router(main_router)