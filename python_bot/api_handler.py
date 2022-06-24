import requests

BASE_URL = "http://localhost:3000"


def get_compilations():
    COMPILATIONS_PATH = BASE_URL + "/compilation"
    response = requests.get(COMPILATIONS_PATH)
    result = response.json()
    print(result)
    return result


USER_PATH = BASE_URL + "/user"


def add_new_user(chat_id, username):
    """Если успешно, 201, если уже есть 409, неверные данные 400"""
    data = {'nickname': username, 'user_id': chat_id}
    response = requests.post(USER_PATH, json=data)
    return response.status_code


PLAYLIST_PATH = BASE_URL + "/playlist"


def add_album(creator, title, description=None, cover=None):
    data = {'creator': creator, 'title': title, 'is_album': True}
    if description is not None:
        data['description'] = description
    if cover is not None:
        data['cover'] = cover
    response = requests.post(PLAYLIST_PATH, json=data)
    return response.status_code


FUNCTIONS_PATH = BASE_URL + "/rpc"


def make_artist(chat_id):
    function_name = 'make_artist'
    response = requests.get(FUNCTIONS_PATH + function_name, params={"user_id": chat_id})
    return response.status_code


def is_artist(chat_id):
    function_name = 'is_artist'
    response = requests.get(FUNCTIONS_PATH + function_name, params={"user_id": chat_id})
    if response.status_code == 200:
        return bool(response.json())
    return False


def user_registered(chat_id):
    function_name = '/user_registered'
    response = requests.get(FUNCTIONS_PATH + function_name, params={"user_id": chat_id})
    if response.status_code == 200:
        return bool(response.json())
    return False
