from typing import Annotated
from fastapi import FastAPI, UploadFile, Response, status, File
from fastapi.encoders import jsonable_encoder

from config import *
from pipeline import *
from utils import convert_file

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "fastapi, use /docs"}


@app.put('/add-context-url')
def add_context_url(collection: str, url: str, response: Response):
    try:
        res = load_url_pipeline(collection, url)
        return jsonable_encoder({'result': str('Doc chunks:', len(res.to_list()))})
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return jsonable_encoder({'result', str(e)})


@app.put('/add-context-file')
def add_context_file(collection: str, file: Annotated[bytes, File()], filetype: str, response: Response):
    try:
        filename = 'temp'
        convert_file(file, filename, filetype)

        res = load_file_pipeline(collection, filename)
        print('Doc chunks inserted:', len(res.to_list()))
        return jsonable_encoder({'result': str('Doc chunks:', len(res.to_list()))})
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return jsonable_encoder({'result', str(e)})


@app.get('/get-doc')
def get_doc(collection: str, query: str, response: Response):
    try:
        res = query_pipeline(collection, query).get_dict()

        return jsonable_encoder({'result': res['text']})

    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return jsonable_encoder({'result', str(e)})


@app.get('/answer')
def do_answer_api(collection: str, session_id: str, query: str, response: Response):
    try:
        res = chat_pipeline(collection, query, session_id).get_dict()

        return jsonable_encoder({'result': res['answer']})

    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return jsonable_encoder({'result', str(e)})
