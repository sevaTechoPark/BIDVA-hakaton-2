import os
from docx2pdf import convert # word
import fitz # pdf

def word_to_pdf(file_path):
    """
    Функция конвертирует .docx в .pdf
    """
    # Получаем имя файла
    name = os.path.splitext(os.path.basename(file_path))[0]
    output = f"{name}.pdf"

    # Конвертируем файл
    try:
        convert(file_path, output)
        print(f"Успешно преобразован {file_path} в {output}")
    except Exception as e:
        print(f"Ошибка при преобразовании: {e}")
        

def pdf_to_dict(file_path, articles_dict):
    """
    Функция добавляет данные статьи из PDF-файла в заданный словарь.
    Формат записи в словарь: {ссылка: [автор, дата, текст]}
    """
    with fitz.open(file_path) as doc:
        # Временный словарь для сбора данных статьи
        extracted_data = {}
        
        # Получаем текст со всех страниц документа
        content_lines = []
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            content_lines.extend([line.strip() for line in page.get_text("text").split("\n") if line.strip()])
        
        # Собираем заголовочную информацию
        extracted_data["link"] = content_lines[0]
        extracted_data["author"] = content_lines[1]
        extracted_data["publication_date"] = content_lines[2]
        # Начиная с 3 строки идет текст статьи
        content_lines = content_lines[3:]
        extracted_data["text"] = '\n'.join(content_lines)
        
        # Вставляем данные в переданный сверху словарь
        articles_dict[extracted_data["link"]] = [
            extracted_data["author"],
            extracted_data["publication_date"],
            extracted_data["text"]
        ]
    
    return articles_dict