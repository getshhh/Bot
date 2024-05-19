from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def create_main_kb(is_admin: bool) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    if is_admin:
        markup.add(KeyboardButton('Админ панель'))
    markup.add(KeyboardButton('Задания'))
    markup.add(KeyboardButton('Баланс'))
    markup.add(KeyboardButton('Профиль'))
    return markup


def create_task_kb() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton('Wow-Task'))
    markup.add(KeyboardButton('Easy-Task 1'))
    markup.add(KeyboardButton('Easy-Task 2'))
    markup.add(KeyboardButton('Easy-Task 3'))
    markup.add(KeyboardButton('В главное меню'))
    return markup
