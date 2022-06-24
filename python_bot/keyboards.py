import telebot

import constants as const
back_btn = telebot.types.KeyboardButton('На главную')

main_menu_btn_1 = telebot.types.KeyboardButton('Подборки')
main_menu_btn_2 = telebot.types.KeyboardButton('Мои плейлисты')
main_menu_btn_3 = telebot.types.KeyboardButton('Новости')
main_menu_btn_4 = telebot.types.KeyboardButton('Создать плейлист')
main_menu_btn_5 = telebot.types.KeyboardButton(const.ARTIST_MENU)


def get_main_menu(is_artist):
    main_menu = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=2)
    main_menu.add(main_menu_btn_1, main_menu_btn_2, main_menu_btn_3, main_menu_btn_4)
    if is_artist:
        main_menu.add(main_menu_btn_5)
    return main_menu


playlists_menu = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=2)

playlists_menu_btn_1 = telebot.types.KeyboardButton('Вперед')
playlists_menu_btn_2 = telebot.types.KeyboardButton('Назад')

playlists_menu.add(playlists_menu_btn_1, back_btn)

delete_menu = telebot.types.ReplyKeyboardRemove()
