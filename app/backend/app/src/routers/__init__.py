from fastapi import APIRouter

from src.routers.rag import router as rag_router

main_router = APIRouter()

main_router.include_router(rag_router)