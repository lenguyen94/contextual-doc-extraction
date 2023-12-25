import os
from dotenv import load_dotenv

load_dotenv()

# credentials
DB_TYPE = os.getenv('DB_TYPE')  # tested with postgres & sqlite
DB_URL = os.getenv('DB_URL')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
MILVUS_URI = os.getenv('MILVUS_URI')
[MILVUS_HOST, MILVUS_PORT] = MILVUS_URI.split('://')[1].split(':')

# default settings
DROP_EXIST = True
EMBED_MODEL = 'all-mpnet-base-v2'
DIM = 768
LLM_NAME = 'gpt-3.5-turbo'

