import os

from fastapi import APIRouter, HTTPException, File, UploadFile
from fastapi.responses import FileResponse

from src.models import server_model
from src.schemas.server import RagResponseSchema
from src.schemas.server import RagRequestSchema

router = APIRouter(prefix="", tags=["RAG-модель"])

@router.post(
    '/rag',
    tags=["Use"],
    summary='Запрос пользователя на summary',
    response_model=RagResponseSchema
)
def get_summary(request: RagRequestSchema):
    return server_model.get_sammary(request)

@router.get(
    '/articles_template',
    tags=["Learn"],
    summary="Получить шаблон для загрузки статьи"
)
def download_file():

    file_full_name = './src/article_temp.pdf'

    if not os.path.exists(file_full_name):
        raise HTTPException(status_code=404, detail="Файл не найден")
    
    return FileResponse(
        file_full_name,
        media_type='application/pdf'
    )

@router.post(
    '/articles',
    tags=["Learn"],
    summary="Загрузить статьи в формате PDF"
)
def upload_file(uploaded_files: list[UploadFile]):
    server_model.upload_files_to_vbd(uploaded_files)
    return {
        "status": "success",
        "message": "Дкйствие выпорлнено"
    }
    