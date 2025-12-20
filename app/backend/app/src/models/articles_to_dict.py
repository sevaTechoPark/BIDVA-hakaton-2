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
        

def pdf_to_dict(file_path):
    """
    Функция добавляет данные статьи из PDF-файла в заданный словарь.
    Формат записи в словарь: {ссылка: [автор, дата, текст]}
    """
    block_content = []
    with fitz.open(file_path) as doc:
        # Временный словарь для сбора данных статьи
        extracted_data = {}
        
        # Получаем текст со всех страниц документа
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)

            for block in page.get_text("blocks"):
                block_content.append(block[4].replace("\n", ""))

    #Формируем результат
    return {
        'link': block_content[0],
        'author': block_content[1],
        'publication_date': block_content[2],
        'text': '\n'.join(block_content[3:])
    }