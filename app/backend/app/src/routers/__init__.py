from fastapi import APIRouter

from src.routers.server_api import router as rag_router

main_router = APIRouter()

main_router.include_router(rag_router)