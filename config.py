import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    MODEL = os.getenv("OPENAI_MODEL")
    BASE_URL = os.getenv("OPENAI_BASE_URL")
    API_KEY = os.getenv("OPENAI_API_KEY")
    INDEX_NAME=os.getenv("INDEX_NAME")
    PREFIX=os.getenv("PREFIX")
    DISTANCE_METRIC = os.getenv("DISTANCE_METRIC")
    REDIS_HOST = os.getenv("REDIS_HOST")
    REDIS_PORT = os.getenv("REDIS_PORT")
    REDIS_PASSWORD=os.getenv("")


