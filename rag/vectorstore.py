import weaviate
from langchain.vectorstores import Weaviate


class Store:
    def __init__(self, class_name, url="http://0.0.0.0:8080") -> None:
        self.client = weaviate.Client(url=url)
        self.db = Weaviate(client=self.client, index_name=class_name, text_key="description")
    
    def add_text(self, input_query):
        self.db.add_texts(texts=[input_query])

    def similarity_search(self, input_query, limit=1):
        return self.db.similarity_search(input_query, k=limit)

    def get_db(self):
        return self.db
