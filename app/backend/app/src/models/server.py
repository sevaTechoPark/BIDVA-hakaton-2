import os

from src.schemas.server import RagRequestSchema
from src.schemas.server import RagResponseSchema
from src.schemas.data_base import ChankSchema
from src.schemas.data_base import SearchSchema

from src.models.text_preparetion import TextPreparetion
from src.models.transformer import Transformer
from src.models.pdf_reader import Pdf_Reader
from src.models.data_base import Qdrant_db
from src.models.giga_api import Giga_LLM

class Model():

    def __init__(self):
        """
        Конструктор класса
        """
        self.__transformer = Transformer()
        self.__text_prepare = TextPreparetion()
        self.__pdf_reader = Pdf_Reader()
        self.__qdrant_db = Qdrant_db(self.__transformer.get_vector_len())
        self.__llm = Giga_LLM()
        pass

    def upload_files_to_vbd(self, files:list):
        """
        Загрузка файлов в векторную БД
        Parameters: 
            files (list(UploadFile)): Массив файлов
        """
        bd_test = list()
        for file in files:
            # Читаем файл и получаем содержимое статьи
            article = self.__pdf_reader.get_content_by_file(file)
            # Текст статьи делим на чанки
            chanks = self.__text_prepare.split_chancs(article.content)

            for chank in chanks:
                # Текст каждого чанка унифицируем
                sentense = self.__text_prepare.prepare(chank)
                # Преобразуем текст чанка в вектор
                embedding_vector = self.__transformer.encode(sentense)
                # Сохраняем в БД
                self.__qdrant_db.save_chank(ChankSchema(
                    link = article.link,
                    author = article.author,
                    publication_date = article.publication_date,
                    text = chank,
                    embedding = embedding_vector
                ))

    def get_sammary(self, request:RagRequestSchema)->RagResponseSchema:
        """
        Получить краткое содержимое статей по запросу
        Parameters: 
            request (RagRequestSchema): Запрос пользователя
        """

        # Унифицируем текст запроса
        sentense = self.__text_prepare.prepare(request.request_text)
        # Преобразуем запрос в вектор
        embedding_vector = self.__transformer.encode(sentense)
        # Выполняем поиск чанков
        chanks = self.__qdrant_db.similar_search(
            SearchSchema(
                author=request.filter.author,
                start_date=request.filter.start_date,
                end_date=request.filter.end_date,
                embedding=embedding_vector
            )
        )

        if len(chanks) == 0:
            return RagResponseSchema(
                links=list(),
                text="В базе не найдены статьи на заданную тему.\nПопробуйте изменить запрос или добавить новые статьи связанные с даннй темой."
            )
        
        links = list()
        context = str()
        context_limit = 1000

        for chank in chanks:
            if len(context) > context_limit:
                break

            links.append(chank.link)
            context = context + chank.text + "\n"

        return RagResponseSchema(
            text=self.__llm.get_summary(context=context, question=request.filter.create_test),
            links=list(set(links))
        )