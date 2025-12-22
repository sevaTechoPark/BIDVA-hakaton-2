import uuid
import datetime

from qdrant_client import QdrantClient, models

from src.schemas.data_base import ChankSchema
from src.schemas.data_base import SearchSchema

class Qdrant_db():

    __CLIENT_URL = 'http://localhost:6333'
    __COLLECTION_NAME = 'Articles'

    def __init__(self, vector_len:int):
        self.qdrant_client = QdrantClient(self.__CLIENT_URL)
        self.collection = self.__init_collection(self.__COLLECTION_NAME, vector_len)

    def save_chank(self, data:ChankSchema):

        self.qdrant_client.upsert(
            collection_name = self.__COLLECTION_NAME,
            points = [
                models.PointStruct(
                    id = str(uuid.uuid4()),
                    vector = data.embedding,
                    payload = {
                        "link": data.link,
                        "author": data.author,
                        "date": data.publication_date.isoformat(),
                        "content": data.text
                    }
                )
            ]
        )

    def similar_search(self, filters:SearchSchema)->list[ChankSchema]:

        must_conditions = []
    
        if filters.author:
            must_conditions.append(
                models.FieldCondition(
                    key="author",
                    match=models.MatchValue(value=filters.author)
                )
            )
        
        if filters.start_date or filters.end_date:
            range_condition = {}
            if filters.start_date:
                range_condition["gte"] =filters.start_date.isoformat()
            if filters.end_date:
                range_condition["lte"] = filters.end_date.isoformat()
            
            must_conditions.append(
                models.FieldCondition(
                    key="publication_date",
                    range=models.Range(**range_condition)
                )
            )
        
        query_filter = models.Filter(must=must_conditions) if must_conditions else None
        
        query_points = self.qdrant_client.query_points(
            collection_name=self.__COLLECTION_NAME,
            query=filters.embedding,
            query_filter=query_filter,
            with_payload=True,
            with_vectors=False
        )

        chanks = list()
        for point in query_points.points:
            chanks.append(
                ChankSchema(
                    link=point.payload["link"],
                    author=point.payload["author"],
                    text=point.payload["content"],
                )
            )
        
        return chanks

    def __init_collection(self, collection_name:str, vector_len:int):
        """
        Создание новой коллекции в БД, при её отсутствии
        Parameters: 
            collection_name (string): Название коллекции
            vector_len (int): Длина вектора
        """

        if not self.qdrant_client.collection_exists(collection_name = collection_name):
            self.qdrant_client.create_collection(
                collection_name = collection_name,
                vectors_config = models.VectorParams(
                    size = vector_len,
                    distance = models.Distance.COSINE
                ),
            )
