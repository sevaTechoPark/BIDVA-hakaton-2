import os

from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole

class Giga_LLM():

    def __init__(self):
        # Читаем токен из переменной среды
        GIGA_TOKEN = os.getenv('GIGA_TOKEN')
        if not GIGA_TOKEN:
            raise RuntimeError('GIGA_TOKEN is not set in environment variables!')

        self.giga_model = GigaChat(
            credentials=GIGA_TOKEN,
            scope="GIGACHAT_API_PERS",
            model="GigaChat-2",
            verify_ssl_certs=False
        )
    
    def get_summary(self, context:str, question=False)->str:
        
        llm_request = [
            Messages(role=MessagesRole.SYSTEM, content=self.__get_head_prompt(question=question)),
            Messages(role=MessagesRole.USER, content=context)
        ]

        response = self.__get_llm_response(llm_request)

        return response.choices[0].message.content

    def __get_llm_response(self, request_text:list)->str:

        chat_object = Chat(
            messages=request_text,
            #max_tokens=100,               # Максимальная цена запроса (походу не работает, тратит больше)
            temperature=0.0,              # Максимальная строгость, без творчества
            top_p=0.1,                    # Только самые распространенные ответы
            presence_penalty=2.0,         # Гарантирует использование только имеющихся фактов, без фантазии
            frequency_penalty=0.5         # Небольшой штраф за повторение
        )
        
        # Генерируем ответ
        return self.giga_model.chat(chat_object)
    
    def __get_head_prompt(self, question=False):

        main_prompt =  """
        Необходимо на основе контекста сформировать краткий пересказ.
        Повествование ответа должно быть логически верным.
        В ответе необходимо привести точные цитаты без искажения текста.
        """
        if question:
            main_prompt += "\nНа основе контекста необходимо сформировать небольшой тест."

        return question
