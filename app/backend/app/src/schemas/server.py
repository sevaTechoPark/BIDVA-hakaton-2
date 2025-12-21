from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class FilterSchema(BaseModel):
    author: Optional[str] = None #= Field(title="Автор статьи")
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    create_test: Optional[bool] = None

class RagResponseSchema(BaseModel):
    text: str = Field(title="Ответ LLM на запрос порльзователя")
    links: list = Field(title="Ссылки на статьи")

class RagRequestSchema(BaseModel):
    filter: Optional[FilterSchema] = None#= Field(title="Фильтры", description="Фильтры для поиска статей")
    request_text: str = Field(title="Запрос пользователя", description="Основной запрос пользователя на какую тему необходимо сформировать аннотацию")

class ArticleSchema(BaseModel):
    link: str = Field(title="Ссылка на статю")
    author: str | None = Field(title="Автор статьи")
    publication_date: datetime | None = Field(title="Дата публикации")
    content: str = Field(title="Содержимое статьи")