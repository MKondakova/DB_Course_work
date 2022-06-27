import genre as genre
import telebot as tb
import api_handler as api
import keyboards as kb

from config import TOKEN
from constants import WELCOME_MESSAGE, ERROR_MESSAGE
import constants as const

bot = tb.TeleBot(TOKEN)

artist_set: set = set()
user_names = {}

get_main_menu = lambda cid: kb.get_main_menu(cid in artist_set)


def get_username(message):
    cid = message.chat.id
    if message.content_type == "text":
        text = message.text
        if text == '.':
            text = message.from_user.username
        status_code = api.add_new_user(cid, text)
        if status_code != 201:
            bot.send_message(cid, ERROR_MESSAGE)
        else:
            msg = bot.send_message(cid, f"Здравствуй, {text}", reply_markup=kb.get_main_menu(cid in artist_set))
            bot.register_next_step_handler(msg, handle_main_menu)
    else:
        markup = tb.types.ForceReply(selective=False)
        msg = bot.send_message(cid, "Введи своё имя или '.' если хочешь взять ник", reply_markup=markup)
        bot.register_next_step_handler(msg, get_username)


def delete_playlist(cid, playlists):
    msg = bot.send_message(cid, "Введи номер или . если передумал")
    bot.register_next_step_handler(msg, handle_playlist_d_number, playlists)


def handle_playlist_d_number(message, playlists):
    if message.content_type == 'text' and len(message.text.strip()) > 0:
        if message.text.strip() == '.':
            msg = bot.send_message(message.chat.id,
                                   const.CANSEL_MESSAGE,
                                   reply_markup=kb.artist_menu)
            bot.register_next_step_handler(msg, handle_albums_menu, playlists)
            return
        if message.text.strip().isdigit():
            number = int(message.text.strip())
            if 1 <= number <= len(playlists):
                status = api.delete_playlist(playlists[number - 1]['id'])
                msg_text = const.SUCCESS_MESSAGE if status else ERROR_MESSAGE
                msg = bot.send_message(message.chat.id, msg_text, reply_markup=kb.artist_menu)
                bot.register_next_step_handler(msg, handle_artist_menu)
                return
    delete_playlist(message.chat.id, playlists)


def show_playlists(playlists, cid, is_albums):
    msg_text = ""
    if len(playlists) == 0:
        msg_text = const.EMPTY_MESSAGE
    else:
        i = 1
        for playlist in playlists:
            msg_text += ('🤫 ' if playlist['is_private'] else "") + str(i) + '. ' + playlist['title'] + "\n"
            i += 1
    variation = int(is_albums)
    markup = [kb.playlists_menu, kb.albums_menu]
    handler = [None, handle_albums_menu]
    msg = bot.send_message(cid, msg_text, reply_markup=markup[variation])
    bot.register_next_step_handler(msg, handler[variation], playlists)


def load_song(message):
    cid = message.chat.id
    msg = bot.send_message(cid, "Введи название композиции или . для отмены",
                           reply_markup=kb.delete_menu)
    bot.register_next_step_handler(msg, handle_song_title)


def handle_song_title(message):
    if message.content_type == 'text' and len(message.text.strip()) > 0:
        if message.text.strip() == '.':
            msg = bot.send_message(message.chat.id,
                                   const.CANSEL_MESSAGE,
                                   reply_markup=kb.artist_menu)
            bot.register_next_step_handler(msg, handle_artist_menu)
            return
        title = message.text.strip()
        msg = bot.reply_to(message, "Отправь аудиофайл или . для отмены")
        bot.register_next_step_handler(msg, handle_song_file, title)
    else:
        load_song(message)


def handle_song_file(message, title):
    if message.content_type == 'audio':
        file_id = message.audio.file_id
        get_song_album(message, title, file_id)
        return
    if message.content_type == 'text' and len(message.text.strip()) > 0:
        if message.text.strip() == '.':
            msg = bot.send_message(message.chat.id,
                                   const.CANSEL_MESSAGE,
                                   reply_markup=kb.artist_menu)
            bot.register_next_step_handler(msg, handle_artist_menu)
            return
    msg = bot.reply_to(message, "Отправь аудиофайл или . для отмены")
    bot.register_next_step_handler(msg, handle_song_file, title)


def get_song_album(message, title, file_id):
    cid = message.chat.id
    albums = api.get_albums(cid)
    if len(albums) > 0:
        bot.reply_to(message, "Выбери альбом из списка и введи номер или . для отмены")
        msg_text = ""
        i = 1
        for album in albums:
            msg_text += str(i) + ". " + album['title'] + '\n'
            i += 1
        msg = bot.send_message(message.chat.id, msg_text)
        bot.register_next_step_handler(msg, handle_song_album, title, file_id, albums)
    else:
        msg = bot.reply_to(message, "Сперва нужно добавить альбом", reply_markup=kb.artist_menu)
        bot.register_next_step_handler(msg, handle_artist_menu)


def handle_song_album(message, title, file_id, albums):
    if message.content_type == 'text' and len(message.text.strip()) > 0:
        if message.text.strip() == '.':
            msg = bot.send_message(message.chat.id,
                                   const.CANSEL_MESSAGE,
                                   reply_markup=kb.artist_menu)
            bot.register_next_step_handler(msg, handle_artist_menu)
            return
        if message.text.strip().isdigit():
            number = int(message.text.strip())
            if 1 <= number <= len(albums):
                get_song_genre(message, title, file_id, albums[number - 1]['id'])
                return
    get_song_album(message, title, file_id)


def get_song_genre(message, title, file_id, album):
    genres = api.get_genres()
    if len(genres) > 0:
        bot.reply_to(message, "Выбери жанр из списка и введи номер или отправь . чтобы пропустить")
        msg_text = ""
        i = 1
        for genre in genres:
            msg_text += str(i) + ". " + genre['name'] + '\n'
            i += 1
        msg = bot.send_message(message.chat.id, msg_text)
        bot.register_next_step_handler(msg, handle_song_genre, title, file_id, album, genres)
    else:
        get_song_lyrics(message.chat.id, title, file_id, album, None)


def handle_song_genre(message, title, file_id, album, genres):
    if message.content_type == 'text' and len(message.text.strip()) > 0 and message.text.strip().isdigit():
        number = int(message.text.strip())
        if 1 <= number <= len(genres):
            get_song_lyrics(message.chat.id, title, file_id, album, genres[number - 1]['id'])
            return

    get_song_genre(message, title, file_id, album)


def get_song_lyrics(chat_id, title, file_id, album, genre):
    msg = bot.send_message(chat_id, "Отправь текст композиции или . чтобы пропустить")
    bot.register_next_step_handler(msg, handle_song_lyrics, title, file_id, album, genre)


def handle_song_lyrics(message, title, file_id, album, genre):
    if message.content_type == "text":
        lyrics = message.text.strip()
        if len(lyrics) > 0:
            status_code = api.add_song(message.chat.id, album, title, file_id, genre, None if lyrics == '.' else lyrics)
            msg_text = const.SUCCESS_MESSAGE if 200 <= status_code <= 205 else ERROR_MESSAGE
            msg = bot.send_message(message.chat.id, msg_text, reply_markup=kb.artist_menu)
            bot.register_next_step_handler(msg, handle_artist_menu)
            return
    get_song_lyrics(message.chat.id, title, file_id, album, genre)


def create_playlist(message, is_album=False):
    cid = message.chat.id
    get_playlist_name(cid, is_album)
    return


def get_playlist_name(cid, is_album=False):
    playlist_name = 'альбома' if is_album else 'плейлиста'
    msg = bot.send_message(cid, "Введи название " + playlist_name, reply_markup=kb.delete_menu)
    bot.register_next_step_handler(msg, handle_playlist_name, is_album)


def get_playlist_description(cid, is_album, title):
    playlist_name = 'альбома' if is_album else 'плейлиста'
    msg = bot.send_message(cid, "Введи описание " + playlist_name + ' или "." чтобы пропустить',
                           reply_markup=kb.delete_menu)
    bot.register_next_step_handler(msg, handle_playlist_description, is_album, title)


def get_playlist_cover(cid, is_album, title, playlist_description):
    playlist_name = 'альбома' if is_album else 'плейлиста'
    msg = bot.send_message(cid, "Отправь обложку " + playlist_name + ' или "." чтобы пропустить',
                           reply_markup=kb.delete_menu)
    bot.register_next_step_handler(msg, handle_playlist_cover, is_album, title, playlist_description)


def handle_playlist_name(message, is_album):
    cid = message.chat.id
    if message.content_type == "text":
        playlist_name = message.text.strip()
        if len(playlist_name) > 0:
            get_playlist_description(cid, is_album, playlist_name)
            return
    get_playlist_name(cid, is_album)


def handle_playlist_description(message, is_album, title):
    cid = message.chat.id
    if message.content_type == "text":
        playlist_description = message.text.strip()
        if len(playlist_description) > 0:
            get_playlist_cover(cid, is_album, title,
                               None if playlist_description == '.' else playlist_description)
            return

    get_playlist_description(cid, is_album, title)


def handle_playlist_cover(message, is_album, title, playlist_description):
    cid = message.chat.id
    handler = [handle_main_menu, handle_artist_menu]
    markup = [get_main_menu(cid), kb.artist_menu]
    variation = int(is_album)
    status_code = None
    if message.content_type == "text" and message.text.strip() == '.':
        status_code = api.add_playlist(cid, title, playlist_description, None, is_album)
    elif message.content_type == 'photo':
        photo_id = message.photo[len(message.photo) - 1].file_id
        status_code = api.add_playlist(cid, title, playlist_description, photo_id, is_album)
    if status_code is not None:
        msg = bot.send_message(cid, const.SUCCESS_MESSAGE if 200 <= status_code <= 205 else ERROR_MESSAGE,
                               reply_markup=markup[variation])
        bot.register_next_step_handler(msg, handler[variation])
        return
    get_playlist_cover(cid, is_album, title, playlist_description)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    cid = message.chat.id
    user_info = api.user_registered(cid)
    if not user_info:
        bot.reply_to(message, WELCOME_MESSAGE)
        markup = tb.types.ForceReply(selective=False)
        msg = bot.send_message(cid, "Введи своё имя или '.' если хочешь взять ник", reply_markup=markup)
        bot.register_next_step_handler(msg, get_username)
        return
    if cid not in artist_set and user_info[0]['is_artist']:
        artist_set.add(cid)
    if cid not in user_names:
        user_names[cid] = user_info[0]['nickname']
    api.make_artist(cid)

    msg = bot.reply_to(message, f"Здравствуй, {user_info[0]['nickname']})",
                       reply_markup=get_main_menu(cid))
    bot.register_next_step_handler(msg, handle_main_menu)


@bot.message_handler(regexp=".*")
def handle_massage(message):
    send_welcome(message)


def handle_main_menu(message):
    cid = message.chat.id
    if message.text.strip() == const.CREATE_PLAYLIST:
        create_playlist(message, False)
    elif message.text.strip() == const.MY_PLAYLISTS:
        my_playlists = api.get_playlists(message.chat.id)
        show_playlists(my_playlists, message.chat.id, False)
    elif message.text.strip() == const.ARTIST_MENU and cid in artist_set:
        msg = bot.send_message(cid, const.SELECT_ACTION_MESSAGE, reply_markup=kb.artist_menu)
        bot.register_next_step_handler(msg, handle_artist_menu)
    elif message.text.strip() == "Обнови":
        send_welcome(message)
    else:
        msg = bot.send_message(cid, "Что-то я не понял", reply_markup=get_main_menu(message.chat.id))
        bot.register_next_step_handler(msg, handle_main_menu)


def handle_artist_menu(message):
    cid = message.chat.id
    if message.text.strip() == const.CREATE_ALBUM:
        create_playlist(message, True)
    elif message.text.strip() == const.MAIN_PAGE:
        msg = bot.send_message(cid, const.GO_MAIN_MENU, reply_markup=get_main_menu(cid))
        bot.register_next_step_handler(msg, handle_main_menu)
    elif message.text.strip() == const.MY_ALBUMS:
        my_albums = api.get_albums(cid)
        show_playlists(my_albums, cid, True)
    elif message.text.strip() == const.LOAD_SONG:
        load_song(message)
    else:
        msg = bot.send_message(cid, "Что-то я не понял", reply_markup=kb.artist_menu)
        bot.register_next_step_handler(msg, handle_artist_menu)


def handle_albums_menu(message, playlists):
    cid = message.chat.id
    if message.text.strip() == const.BACK_MESSAGE:
        msg = bot.send_message(cid, const.SELECT_ACTION_MESSAGE, reply_markup=kb.artist_menu)
        bot.register_next_step_handler(msg, handle_artist_menu)
    elif message.text.strip() == const.OPEN_ALBUM:
        open_playlist(message.chat.id, playlists)
    elif message.text.strip() == const.DELETE_ALBUM:
        delete_playlist(message.chat.id, playlists)
    else:
        msg = bot.send_message(cid, "Что-то я не понял", reply_markup=kb.albums_menu)
        bot.register_next_step_handler(msg, handle_albums_menu, playlists)


def handle_playlists_menu(message, playlists):
    cid = message.chat.id
    if message.text.strip() == const.BACK_MESSAGE:
        msg = bot.send_message(cid, const.SELECT_ACTION_MESSAGE, reply_markup=get_main_menu(message.chat.id))
        bot.register_next_step_handler(msg, handle_main_menu)
    elif message.text.strip() == const.OPEN_ALBUM:
        open_playlist(message.chat.id, playlists)
    elif message.text.strip() == const.DELETE_ALBUM:
        delete_playlist(message.chat.id, playlists)
    else:
        msg = bot.send_message(cid, "Что-то я не понял", reply_markup=kb.albums_menu)
        bot.register_next_step_handler(msg, handle_albums_menu, playlists)


def open_playlist(cid, playlists):
    msg = bot.send_message(cid, "Введи номер или . если передумал")
    bot.register_next_step_handler(msg, handle_playlist_o_number, playlists)


def handle_playlist_o_number(message, playlists):
    if message.content_type == 'text' and len(message.text.strip()) > 0:
        if message.text.strip() == '.':
            msg = bot.send_message(message.chat.id,
                                   const.CANSEL_MESSAGE,
                                   reply_markup=kb.artist_menu)
            bot.register_next_step_handler(msg, handle_albums_menu, playlists)
            return
        if message.text.strip().isdigit():
            number = int(message.text.strip())
            if 1 <= number <= len(playlists):
                songs = api.get_songs(playlists[number - 1]['id'])
                playlist = playlists[number - 1]
                show_songs(message.chat.id, songs, playlist)
                return
    open_playlist(message.chat.id, playlists)


def show_songs(cid, songs, playlist):
    markup = [kb.playlist_menu, kb.album_menu]
    handler = handle_playlist_menu
    playlist['songs'] = songs
    print(str(playlist))
    if playlist['cover'] is not None:
        bot.send_photo(cid, playlist['cover'])
    msg_text = ""
    msg_text += playlist['title'] + '\n\n'
    msg_text += (playlist['description'] + '\n\n') if playlist['description'] is not None else ''
    msg_text += '\tКомпозиции:\n'
    if len(songs) == 0:
        msg_text += const.EMPTY_MESSAGE
        msg = bot.send_message(cid, msg_text, reply_markup=markup[int(playlist['is_album'])])
        bot.register_next_step_handler(msg, handler, playlist)
        return
    first_song = None
    for song in songs:
        if song['is_first']:
            first_song = song
            break
    curr_song = first_song
    i = 1
    while curr_song['next'] is not None:
        msg_text += str(i) + '. ' + curr_song['title']
        if curr_song['genre'] is not None:
            msg_text += ' ' + curr_song['genre'] + '\n'
        else:
            msg_text += '\n'
        i += 1
        for s in songs:
            if s['id'] == curr_song['next']:
                curr_song = s
                break
    msg_text += str(i) + '. ' + curr_song['title']
    if curr_song['genre'] is not None:
        msg_text += ' ' + curr_song['genre'] + '\n'
    else:
        msg_text += '\n'
    msg = bot.send_message(cid, msg_text, reply_markup=markup[int(playlist['is_album'])])
    bot.register_next_step_handler(msg, handler, playlist)


def handle_playlist_menu(message, playlist):
    cid = message.chat.id
    if message.text.startswith(const.LISTEN_PLAYLIST[:7]):
        listen_playlist(cid, playlist)
    else:
        msg = bot.send_message(cid, "Что-то я не понял", reply_markup=kb.albums_menu)
        bot.register_next_step_handler(msg, handle_playlist_menu, playlist)


def listen_playlist(chat_id, playlist):
    msg = None
    if len(playlist['songs']) == 0:
        msg = bot.send_message(chat_id, const.EMPTY_MESSAGE, reply_markup=kb.albums_menu)
    for s in playlist['songs']:
        msg = bot.send_audio(chat_id, s['file'], title=s['title'])
    bot.register_next_step_handler(msg, handle_playlist_menu, playlist)


print('Started')
bot.polling()
