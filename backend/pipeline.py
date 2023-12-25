from towhee import pipe, ops, DataCollection

from config import *
from utils import *

load_url_pipeline = (
    pipe.input('collection_name', 'source')
    .map('collection_name', 'collection', create_collection)
    .map('source', 'doc', ops.text_loader())
    .flat_map('doc', 'doc_chunk', ops.text_splitter(chunk_size=300))
    .map('doc_chunk', 'vec', ops.sentence_embedding.sbert(model_name=EMBED_MODEL))
    .map('vec', 'vec', ops.np_normalize())
    .map(('collection_name', 'vec', 'doc_chunk'), 'mr',
         ops.ann_insert.osschat_milvus(host=MILVUS_HOST, port=MILVUS_PORT))
    .output('mr')
)

load_file_pipeline = (
    pipe.input('collection_name', 'source')
    .map('collection_name', 'collection', create_collection)
    .map('source', 'doc', ops.data_loader.text_loader())
    .flat_map('doc', 'doc_chunk', ops.text_splitter(chunk_size=300))
    .map('doc_chunk', 'vec', ops.sentence_embedding.sbert(model_name=EMBED_MODEL))
    .map('vec', 'vec', ops.np_normalize())
    .map(('collection_name', 'vec', 'doc_chunk'), 'mr',
         ops.ann_insert.osschat_milvus(host=MILVUS_HOST, port=MILVUS_PORT))
    .output('mr')
)


query_pipeline = (
    pipe.input('collection_name', 'query')
    .map('query', 'query_vec', ops.sentence_embedding.sbert(model_name=EMBED_MODEL))
    .map('query_vec', 'query_vec', ops.np_normalize())
    .map(('collection_name', 'query_vec'), 'search_res',
         ops.ann_search.osschat_milvus(host=MILVUS_HOST,
                                       port=MILVUS_PORT,
                                       **{'metric_type': 'IP', 'limit': 3, 'output_fields': ['text']}))
    .map('search_res', 'text', lambda y: [x[2] for x in y])
    .output('text')
)


chat_pipeline = (
    pipe.input('collection_name', 'query', 'session')
    .map('query', 'query_vec', ops.sentence_embedding.sbert(model_name=EMBED_MODEL))
    .map('query_vec', 'query_vec', ops.np_normalize())
    .map(('collection_name', 'query_vec'), 'search_res',
         ops.ann_search.osschat_milvus(host=MILVUS_HOST,
                                       port=MILVUS_PORT,
                                       **{'metric_type': 'IP', 'limit': 3, 'output_fields': ['text']}))
    .map('search_res', 'knowledge', lambda y: [x[2] for x in y])
    .map(('collection_name', 'session'), 'history',
         ops.chat_message_histories.sql(method='get', db_type=DB_TYPE, url=DB_URL))
    .map(('query', 'knowledge', 'history'), 'messages', ops.prompt.question_answer())
    .map('messages', 'answer', ops.LLM.OpenAI(api_key=OPENAI_API_KEY, model_name=LLM_NAME, temperature=0.8))
    .map(('collection_name', 'session', 'query', 'answer'), 'new_history',
         ops.chat_message_histories.sql(method='add', db_type=DB_TYPE, url=DB_URL))
    .output('query', 'history', 'answer')
)
