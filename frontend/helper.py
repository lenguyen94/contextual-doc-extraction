import uuid

import requests

from config import API_URL


def create_session_id():
    return 's_' + str(uuid.uuid4()).replace('-', '')


def respond(session_id, collection, message, chat_history_1, chat_history_2):
    chat_history_1 = respond_doc(session_id, collection, message, chat_history_1)
    chat_history_2 = respond_chat(session_id, collection, message, chat_history_2)

    return "", chat_history_1, chat_history_2


def respond_chat(session_id, collection, message, chat_history):
    try:
        print(session_id)
        response = requests.get(API_URL + '/answer', params={
            'session_id': session_id, 'query': message, 'collection': collection
        }).json()
        # print(response)
        chat_history.append((message, response['result']))
        # chat_history.append((message, response.get('message')))
    except Exception as e:
        print(e)
    return chat_history


def respond_doc(session_id, collection, message, chat_history):
    try:
        print(session_id)
        response = requests.get(API_URL + '/get-doc', params={
            'query': message, 'collection': collection
        }).json()
        # print(response)
        chat_history.append((message, response['result'][0]))
        # chat_history.append((message, response.get('message')))
    except Exception as e:
        print(e)
    return chat_history


def add_url(session_id, collection, url):
    try:
        print(session_id)
        response = requests.put(API_URL + '/add-context-url', params={
            'session_id': session_id, 'url': url, 'collection': collection
        }).json()
        print(response)
        # chat_history.append((message, response.get('message')))
    except Exception as e:
        print(e)
    return ""


def add_file(session_id, collection, filepath):
    try:
        # print(len(item))
        file = {'file': open(filepath, 'rb')}
        filetype = filepath.split('.')[-1]

        response = requests.put(API_URL + '/add-context-file', files=file,
                                params={'collection': collection, 'session_id': session_id,
                                        'filetype': filetype}).json()
        print(response)
        # chat_history.append((message, response.get('message')))
    except Exception as e:
        print(e)
    return ""
