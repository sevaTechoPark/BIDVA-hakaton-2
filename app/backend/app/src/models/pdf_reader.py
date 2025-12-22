import pymupdf
import io
import dateparser

from fastapi import UploadFile
from datetime import datetime

from src.schemas.server import ArticleSchema

class Pdf_Reader():

    def get_content_by_file_path(self, file_path:str)->ArticleSchema:
        """
        Чтение локального файла PDF 
        Parameters: 
            file_path (string): Полный путь к файлу
        Returns: 
            (ArticleSchema): Содержимое статьи
        """
        pdf_file = pymupdf.open(file_path)
        article_content = self.__pdf_parse(pdf_file)
        pdf_file.close()

        return article_content

    def get_content_by_file(self, file:UploadFile)->ArticleSchema:
        """
        Чтение файла PDF 
        Parameters: 
            file (UploadFile): Файл полученный через API
        Returns: 
            (ArticleSchema): Содержимое статьи
        """

        contents = file.file.read()
        pdf_stream = io.BytesIO(contents)
        pdf_file = pymupdf.open(stream=pdf_stream, filetype="pdf")
        article_content = self.__pdf_parse(pdf_file)
        pdf_file.close()

        return article_content

    def __pdf_parse(self, pdf_file)->ArticleSchema:
        """
        Разбор файла PDF
        Parameters: 
            pdf_file (pymupdf file): Файл pymupdf
        Returns: 
            (ArticleSchema): Содержимое статьи
        """
        block_content = list()

        # Получаем текст со всех страниц документа
        for page_num in range(len(pdf_file)):
            page = pdf_file.load_page(page_num)

            # Получаем все блоки текста со страницы
            for block in page.get_text("blocks"):
                block_content.append(block[4].replace("\n", ""))
        
        # Формируем результат
        return ArticleSchema(
            link=block_content[0],
            author=block_content[1],
            publication_date=self.__date_parse(block_content[2]),
            content='\n'.join(block_content[3:])
        )
    
    def __date_parse(self, date_text:str)->datetime:
        
        settings = {
            'DATE_ORDER': 'DMY',  # день-месяц-год
            'PREFER_DAY_OF_MONTH': 'first',  # для неполных дат
            'TIMEZONE': 'UTC',
        }

        return dateparser.parse(date_text, settings=settings)