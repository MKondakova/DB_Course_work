import requests

BASE_URL = "http://localhost:3000"


def get_compilations():
    COMPILATIONS_PATH = BASE_URL + "/compilation"
    response = requests.get(COMPILATIONS_PATH)
    result = response.json()
    return result


USER_PATH = BASE_URL + "/user"


def add_new_user(chat_id, username):
    """Если успешно, 201, если уже есть 409, неверные данные 400"""
    data = {'nickname': username, 'user_id': chat_id}
    response = requests.post(USER_PATH, json=data)
    return response.status_code


PLAYLIST_PATH = BASE_URL + "/playlist"


def add_playlist(creator, title, description, cover, is_album=False):
    data = {'creator': creator, 'title': title, 'is_album': is_album}
    if description is not None:
        data['description'] = description
    if cover is not None:
        data['cover'] = cover
    response = requests.post(PLAYLIST_PATH, json=data)
    return response.status_code


FUNCTIONS_PATH = BASE_URL + "/rpc"


def make_artist(chat_id):
    function_name = '/make_artist'
    response = requests.post(FUNCTIONS_PATH + function_name, json={"user_id": chat_id})
    return response.status_code


def is_artist(chat_id):
    function_name = '/is_artist'
    response = requests.get(FUNCTIONS_PATH + function_name, params={"user_id": chat_id})
    if response.status_code == 200:
        return bool(response.json())
    return False


def user_registered(chat_id):
    function_name = '/user_registered'
    response = requests.get(FUNCTIONS_PATH + function_name, params={"user_id": chat_id})
    if response.status_code == 200:
        result = response.json()
        return result if len(result) > 0 else False
    return False


def get_playlists(chat_id):
    function_name = '/get_playlists'
    response = requests.get(FUNCTIONS_PATH + function_name, params={"user_id": chat_id})
    if response.status_code == 200:
        return response.json()
    return None


def get_albums(chat_id):
    function_name = '/get_albums'
    response = requests.get(FUNCTIONS_PATH + function_name, params={"user_id": chat_id})
    if response.status_code == 200:
        return response.json()
    return None


def get_genres():
    GENRE_PATH = '/genre'
    response = requests.get(BASE_URL + GENRE_PATH)
    result = response.json()
    return result


def add_song(chat_id, album, title, file_id, genre, lyrics):
    function_name = '/add_song'
    data = {'_user_id': chat_id, 'album': album, '_title': title, '_file': file_id, '_genre': genre, '_lyrics': lyrics}
    response = requests.post(FUNCTIONS_PATH + function_name, json=data)
    print(response.json())
    return response.status_code


def add_song_to_playlist(chat_id, playlist_id, song_id):
    SONGS_PATH = '/song_in_playlist'
    response = requests.post(BASE_URL + SONGS_PATH,
                             json={'playlist_id': playlist_id, 'song_id': song_id, 'user_id': chat_id})
    print(response.json())
    return response.status_code

def delete_playlist(playlist_id):
    response = requests.delete(PLAYLIST_PATH, params={'id': 'eq.' + str(playlist_id)})
    print(response.status_code)
    if response.status_code == 204:
        return True
    return False


def get_songs(playlist_id):
    function_name = '/get_songs'
    response = requests.get(FUNCTIONS_PATH + function_name, params={"playlist_id": playlist_id})
    if response.status_code == 200:
        return response.json()
    return None


def find_songs(title):
    function_name = '/find_songs'
    response = requests.get(FUNCTIONS_PATH + function_name, params={"_title": title})
    if response.status_code == 200:
        return response.json()
    return None
