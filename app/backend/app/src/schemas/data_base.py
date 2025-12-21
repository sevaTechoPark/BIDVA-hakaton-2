from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class ChankSchema(BaseModel):
    link: str = Field(title="Ссылка на статю")
    author: str | None = Field(title="Автор статьи")
    publication_date: Optional[datetime] = None
    text: str = Field(title="Содержимое статьи")
    embedding: Optional[list] = None

class SearchSchema(BaseModel):
    author: str | None = Field(title="Автор статьи")
    start_date: datetime | None = Field(title="Дата с", description="Дата публикации статьи")
    end_date: datetime | None = Field(title="Дата по", description="Дата публикации статьи")
    embedding: list = Field(title="Векторное представление смысла текста")
