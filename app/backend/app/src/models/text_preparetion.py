import string

from pymorphy3 import MorphAnalyzer

class TextPreparetion:

    def __init__(self):
        """
        Конструктор класса
        """
        extended_punctuation = string.punctuation + '«»„“—–…'
        self.punctuation_translater = str.maketrans('', '', extended_punctuation)
        self.morph = MorphAnalyzer()

    def prepare(self, text:str)->str:
        """
        Перевод текста к нижнему регистру;
        Удаление всех знаков препинания;
        Удаление союзов и частиц
        Parameters: 
            text (string): Текст для обработки
        Returns: 
            (string): Очищенный текст
        """
        new_text = text.lower()
        new_text = self.__punctuation_delete(new_text)
        new_text = self.__part_speech_delete(new_text)

        return new_text
    
    def split_chancs(self, text:str, min_chunk_size:int=200, max_chunk_size:int=600)->list:
        """
        Разделение текста на чанки
        Parameters: 
            text (string): Текст для обработки
            min_chunk_size (int): Минимальное количество символов в чанке
            max_chunk_size (int): Максимальное количество символов в чанке
        Returns: 
            (list): Чанки текста
        """

        paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
        chunks = []
        current_chunk = ""
        
        for paragraph in paragraphs:
            # Если абзац слишком большой — разбиваем по длине
            if len(paragraph) > max_chunk_size:
                sub_chunks = self.__chunk_by_length(paragraph, max_chunk_size, 50)
                for sub_chunk in sub_chunks:
                    if len(current_chunk) + len(sub_chunk) <= max_chunk_size:
                        current_chunk += " " + sub_chunk
                    else:
                        if current_chunk:
                            chunks.append(current_chunk.strip())
                        current_chunk = sub_chunk
            else:
                # Обычный абзац
                if len(current_chunk + " " + paragraph) <= max_chunk_size:
                    current_chunk += " " + paragraph
                else:
                    if len(current_chunk) >= min_chunk_size:
                        chunks.append(current_chunk.strip())
                        current_chunk = paragraph
                    else:
                        current_chunk += " " + paragraph
        
        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks

    def __punctuation_delete(self, text:str)->str:
        """
        Удаление всех знаков препинания
        Parameters: 
            text (string): Текст для обработки
        Returns: 
            (string): Очищенный текст
        """
        return text.translate(self.punctuation_translater)

    def __part_speech_delete(self, text:str)->str:
        """
        Удаление союзов и частиц
        Parameters: 
            text (string): Текст для обработки
        Returns: 
            (string): Очищенный текст
        """

        function_pos = {
            'CONJ',   # союзы
            'PRCL',   # частицы
        }

        query_words = text.split()
        result_words_list  = list()

        for word in query_words:
            parsed = self.morph.parse(word)[0]

            if parsed.tag.POS not in function_pos:
                result_words_list.append(word)

        return ' '.join(result_words_list)
    
    def __chunk_by_length(self, text:str, chunk_size:int=500, overlap:int=50)->list:
        """
        Разделение текста на чанки по символам
        Parameters: 
            text (string): Текст для обработки
            chunk_size (int): Размер чанка
            overlap (int): Размер перекрытия текста
        Returns: 
            (list): Чанки текста
        """
        chunks = []
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            start += chunk_size - overlap
        return chunks