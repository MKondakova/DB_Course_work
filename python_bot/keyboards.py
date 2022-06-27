import telebot

import constants as const

go_main_btn = telebot.types.KeyboardButton(const.MAIN_PAGE)
back_button = telebot.types.KeyboardButton(const.BACK_MESSAGE)

main_menu_btn_1 = telebot.types.KeyboardButton(const.COMPILATIONS)
main_menu_btn_2 = telebot.types.KeyboardButton(const.MY_PLAYLISTS)
main_menu_btn_3 = telebot.types.KeyboardButton(const.NEWS)
main_menu_btn_4 = telebot.types.KeyboardButton(const.CREATE_PLAYLIST)
main_menu_btn_5 = telebot.types.KeyboardButton(const.ARTIST_MENU)
main_menu_btn_6 = telebot.types.KeyboardButton(const.SUBSCRIBES)
main_menu_btn_7 = telebot.types.KeyboardButton(const.SEARCH)


def get_main_menu(is_artist):
    main_menu = telebot.types.ReplyKeyboardMarkup(row_width=3, one_time_keyboard=True)
    main_menu.add(main_menu_btn_1, main_menu_btn_2, main_menu_btn_3, main_menu_btn_4, main_menu_btn_6, main_menu_btn_7)
    if is_artist:
        main_menu.add(main_menu_btn_5)
    return main_menu


artist_menu_btn_1 = telebot.types.KeyboardButton(const.CREATE_ALBUM)
artist_menu_btn_2 = telebot.types.KeyboardButton(const.LOAD_SONG)
artist_menu_btn_3 = telebot.types.KeyboardButton(const.MY_ALBUMS)
artist_menu = telebot.types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
artist_menu.add(artist_menu_btn_1, artist_menu_btn_2, artist_menu_btn_3, go_main_btn)


albums_menu = telebot.types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
albums_menu_btn_1 = telebot.types.KeyboardButton(const.OPEN_ALBUM)
albums_menu_btn_2 = telebot.types.KeyboardButton(const.DELETE_ALBUM)
albums_menu.add(albums_menu_btn_1, albums_menu_btn_2, back_button)

playlists_menu = telebot.types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
playlists_menu_btn_1 = telebot.types.KeyboardButton(const.OPEN_PLAYLIST)
playlists_menu_btn_2 = telebot.types.KeyboardButton(const.DELETE_PLAYLIST)
playlists_menu.add(albums_menu_btn_1, albums_menu_btn_2, back_button)

album_menu = telebot.types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
album_menu_btn_1 = telebot.types.KeyboardButton(const.LISTEN_ALBUM)
album_menu_btn_2 = telebot.types.KeyboardButton(const.CHANGE_ORDER)
album_menu_btn_3 = telebot.types.KeyboardButton(const.DELETE_SONG)
album_menu_btn_4 = telebot.types.KeyboardButton(const.EDIT_ALBUM)
album_menu.add(album_menu_btn_1, album_menu_btn_2, album_menu_btn_3, album_menu_btn_4, back_button)

playlist_menu = telebot.types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
playlist_menu_btn_1 = telebot.types.KeyboardButton(const.LISTEN_PLAYLIST)
playlist_menu_btn_2 = telebot.types.KeyboardButton(const.CHANGE_ORDER)
playlist_menu_btn_3 = telebot.types.KeyboardButton(const.DELETE_SONG)
playlist_menu_btn_4 = telebot.types.KeyboardButton(const.EDIT_PLAYLIST)
playlist_menu.add(playlist_menu_btn_1, playlist_menu_btn_2, playlist_menu_btn_3, playlist_menu_btn_4, back_button)

delete_menu = telebot.types.ReplyKeyboardRemove()
