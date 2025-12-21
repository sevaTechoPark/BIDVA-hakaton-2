from sentence_transformers import SentenceTransformer

class Transformer():

    __DEFAULT_TRANSFORMER_NAME = 'ai-forever/ru-en-RoSBERTa'

    def __init__(self):
        self.__model = SentenceTransformer(self.__DEFAULT_TRANSFORMER_NAME)

    def get_vector_len(self):
        """
        Преобразование текста в смысловой вектор
        Returns: 
            (int): Длина вектора
        """

        return self.__model.get_sentence_embedding_dimension()

    def encode(self, text:str)->list:
        """
        Преобразование текста в смысловой вектор
        Parameters: 
            text (string): Текст для преобразования в вектор
        Returns: 
            (list): Вектор чисел
        """
        return self.__model.encode(
            text,
            normalize_embeddings=True,
            convert_to_numpy=False
        ).tolist()