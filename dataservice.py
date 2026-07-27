import numpy as np
from openai import OpenAI



import redis
from pypdf import PdfReader
from redis.commands.search.field import TextField, VectorField
from redis.commands.search.index_definition import IndexDefinition, IndexType
from redis.commands.search.query import Query

from config import Settings
client = OpenAI()

class DataService:
    def __init__(self):
        self.redis_client = redis.Redis(
            host=Settings.REDIS_HOST,
            port=Settings.REDIS_PORT,
            password=Settings.REDIS_PASSWORD,
            decode_responses=False)
    def drop_redis_data(self,index_name: str =Settings.INDEX_NAME):
        try:
            self.redis_client.ft(index_name).dropindex()
            print(f'Dropped {index_name} index')
        except:
            # Index does not exist
            print(f'Failed to drop {index_name} index')

    def load_data_to_redis(self,embeddings):
        # Constants

        vector_dim = len(embeddings[0]['vector'])
        # Initial number of vectors
        vector_number = len(embeddings)

        # Define RedisSearch fields
        text =TextField(name="text")
        text_embedding =VectorField("vector","FLAT",{
            "TYPE":"FLOAT32",
            "DIM":vector_dim,
            "DISTANCE_METRIC": Settings.DISTANCE_METRIC,
            "INITIAL_CAP": vector_number
        })
        fields = [text,text_embedding]

        # Check if index exist
        try:
            self.redis_client.ft(Settings.INDEX_NAME).info()
            print(f'Loaded {embeddings} embeddings')
        except Exception as ex:
            print("No exist :",ex)
            # Create RedisSearch Index
            self.redis_client.ft(Settings.INDEX_NAME).create_index(
                fields=fields,
                definition=IndexDefinition(
                    prefix=[Settings.PREFIX],index_type=IndexType.HASH
                )
            )
            print("Created index")
        for embedding in embeddings:
            key = f"{Settings.PREFIX}:{str(embedding['id'])}"
            embedding["vector"] =np.array(
                embedding["vector"],dtype=np.float32).tobytes()
            print(type(embedding))
            print(embedding.keys())
            print("id:", embedding["id"], type(embedding["id"]))
            print("text:", type(embedding["text"]))
            print("vector:", type(embedding["vector"]))
            print("vector bytes:", len(embedding["vector"]))
            self.redis_client.hset(key,mapping=embedding)
        info = self.redis_client.info()

        keys = info.get("db0", {}).get("keys", 0)
        print(
            f"Loaded {keys} documents into {Settings.INDEX_NAME}")

    def pdf_to_embeddings(self, pdf_path: str, chunk_length: int = 1000):
        # Read data from pdf file and split it into chunks
        reader = PdfReader(pdf_path)
        chunks = []
        for page in reader.pages:
            text_page = page.extract_text()
            chunks.extend([text_page[i:i + chunk_length].replace('\n', '')
                           for i in range(0, len(text_page), chunk_length)])

        # Create embeddings
        response = client.embeddings.create(model='nomic-embed-text:latest', input=chunks)
        return [{'id': value.index, 'vector': value.embedding, 'text': chunks[value.index]} for value in response.data]

    def search_redis(self,
                     user_query: str,
                     index_name: str = "embeddings-index",
                     vector_field: str = "vector",
                     return_fields: list = ["text", "vector_score"],
                     hybrid_fields="*",
                     k: int = 5,
                     print_results: bool = False,
                     ):
        # Creates embedding vector from user query
        embedded_query = client.embeddings.create(input=user_query,
                                                  model="nomic-embed-text:latest").data[0].embedding
        # Prepare the Query
        base_query = f'{hybrid_fields}=>[KNN {k} @{vector_field} $vector AS vector_score]'
        query = (
            Query(base_query)
            .return_fields(*return_fields)
            .sort_by("vector_score")
            .paging(0, k)
            .dialect(2)
        )
        params_dict = {"vector": np.array(
            embedded_query).astype(dtype=np.float32).tobytes()}
        # perform vector search
        results = self.redis_client.ft(index_name).search(query, params_dict)
        if print_results:
            for i, doc in enumerate(results.docs):
                score = 1 - float(doc.vector_score)
                print(f"{i}. {doc.text} (Score: {round(score, 3)})")
        return [doc['text'] for doc in results.docs]