# You Should install for redis
pip install redis
pip install redisearch


# numpy
pip install numpy

# Pdf
pip install pypdf

# OpenIA
pip install openai  

# ENV
pip install python-dotenv

## For Connected RedisInsight
redis (not localhost)

### Example For test
OPENAI_MODEL_CHAT=llama3.2:latest
OPENAI_MODEL_EMBEDDING=nomic-embed-text:latest
OPENAI_BASE_URL="http://localhost:11434/v1"
OPENAI_API_KEY=dummy

INDEX_NAME="embeddings-index"
PREFIX="doc"
DISTANCE_METRIC="COSINE"

REDIS_HOST="localhost"
REDIS_PORT="6379"
REDIS_PASSWORD=