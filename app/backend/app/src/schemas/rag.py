from pydantic import BaseModel, Field
from datetime import datetime

class FilterSchema(BaseModel):
    author: str | None = Field(max_length=100, title="Автор статьи")
    date_from: datetime | None = Field(title="Дата с", description="Дата публикации статьи")
    date_to: datetime | None = Field(title="Дата по", description="Дата публикации статьи")
    create_test: bool = Field(title="Сформировать тест", description="Нужно ли по сгенерированному тексту сформирвоать тест")


class RagResponseSchema(BaseModel):
    filter: FilterSchema = Field(title="Фильтры", description="Фильтры для поиска статей")
    response_text: str = Field(title="Запрос пользователя", description="Основной запрос пользователя на какую тему необходимо сформировать аннотацию")