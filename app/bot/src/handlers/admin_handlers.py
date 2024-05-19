from aiogram import types, Dispatcher

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from src.database.database_func import user_exists, get_user_role, grant_admin_rights
from src.func import generate_unique_code

from src.variables import user_links, user_links_access


async def grant_admin(message: types.Message):
    if grant_admin_rights(message.from_user.id):
        if get_user_role(message.from_user.id) == 'admin':
            await message.answer("Вы получили административные права.")
            await message.answer("Добро пожаловать в админ-панель!")
        else:
            await message.answer("Теперь вы являетесь администратором")
    else:
        await message.answer("У вас недостаточно прав для выполнения этой операции.")


async def admin_panel(message: types.Message):
    if user_exists(message.from_user.id) and get_user_role(message.from_user.id) == 'admin':
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(KeyboardButton('Монеты для Wow-Task'))
        markup.add(KeyboardButton('Монеты для Easy-Task'))
        # markup.add(KeyboardButton('Ссылки для доступа'))
        markup.add(KeyboardButton('В главное меню'))

        await message.answer("Выберите действие:", reply_markup=markup)
    elif get_user_role(message.from_user.id) == 'admin':
        await message.answer("У вас не хватает прав для использования админ-панели.")
    else:
        await message.answer("Вход запрещён.")


# монеты для wow #############################
async def wow_task_coins(message: types.Message):
    if user_exists(message.from_user.id) and get_user_role(message.from_user.id) == 'admin':
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(KeyboardButton('Сгенерировать ссылку на 500 монет'))
        markup.add(KeyboardButton('Сгенерировать ссылку на 600 монет'))
        markup.add(KeyboardButton('Сгенерировать ссылку на 700 монет'))
        markup.add(KeyboardButton('В главное меню'))

        await message.answer("Выберите количество монет для Wow-Task:", reply_markup=markup)
    else:
        await message.answer("У вас нет прав доступа к админ панели.")


async def generate_link_wow_500(message: types.Message):
    if user_exists(message.from_user.id) and get_user_role(message.from_user.id) == 'admin':
        link = generate_unique_code()
        user_links[link] = 500

        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(KeyboardButton('В главное меню'))

        await message.answer(f"Ссылка для получения 500 монет: `{link}`", parse_mode='markdownv2', reply_markup=markup)
    else:
        await message.answer("У вас нет прав доступа к админ панели.")


async def generate_link_wow_600(message: types.Message):
    if user_exists(message.from_user.id) and get_user_role(message.from_user.id) == 'admin':
        link = generate_unique_code()
        user_links[link] = 600

        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(KeyboardButton('В главное меню'))

        await message.answer(f"Ссылка для получения 600 монет: `{link}`", parse_mode='markdownv2', reply_markup=markup)
    else:
        await message.answer("У вас нет прав доступа к админ панели.")


async def generate_link_wow_700(message: types.Message):
    if user_exists(message.from_user.id) and get_user_role(message.from_user.id) == 'admin':
        link = generate_unique_code()
        user_links[link] = 700

        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(KeyboardButton('В главное меню'))

        await message.answer(f"Ссылка для получения 700 монет: `{link}`", parse_mode='markdownv2', reply_markup=markup)
    else:
        await message.answer("У вас нет прав доступа к админ панели.")


# Монеты для easy #############################
async def easy_task_coins(message: types.Message):
    if user_exists(message.from_user.id) and get_user_role(message.from_user.id) == 'admin':
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(KeyboardButton('Сгенерировать ссылку на 200 монет'))
        markup.add(KeyboardButton('Сгенерировать ссылку на 300 монет'))
        markup.add(KeyboardButton('Сгенерировать ссылку на 50 монет'))
        markup.add(KeyboardButton('В главное меню'))

        await message.answer("Выберите количество монет для Wow-Task:", reply_markup=markup)
    else:
        await message.answer("У вас нет прав доступа к админ панели.")


async def generate_link_easy_300(message: types.Message):
    if user_exists(message.from_user.id) and get_user_role(message.from_user.id) == 'admin':
        link = generate_unique_code()
        user_links[link] = 300

        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(KeyboardButton('В главное меню'))

        await message.answer(f"Ссылка для получения 300 монет: `{link}`", parse_mode='markdownv2', reply_markup=markup)
    else:
        await message.answer("У вас нет прав доступа к админ панели.")


async def generate_link_easy_200(message: types.Message):
    if user_exists(message.from_user.id) and get_user_role(message.from_user.id) == 'admin':
        link = generate_unique_code()
        user_links[link] = 200

        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(KeyboardButton('В главное меню'))

        await message.answer(f"Ссылка для получения 200 монет: `{link}`", parse_mode='markdownv2', reply_markup=markup)
    else:
        await message.answer("У вас нет прав доступа к админ панели.")


async def generate_link_easy_50(message: types.Message):
    if user_exists(message.from_user.id) and get_user_role(message.from_user.id) == 'admin':
        link = generate_unique_code()
        user_links[link] = 50

        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(KeyboardButton('В главное меню'))

        await message.answer(f"Ссылка для получения 50 монет: `{link}`", parse_mode='markdownv2', reply_markup=markup)
    else:
        await message.answer("У вас нет прав доступа к админ панели.")


# async def urls_access(message: types.Message):
#     if user_exists(message.from_user.id) and get_user_role(message.from_user.id) == 'admin':
#         markup = ReplyKeyboardMarkup(resize_keyboard=True)
#         markup.add(KeyboardButton('Сгенерировать ссылку на доступ к Easy-Task'))
#
#         await message.answer("Выберите вариант ссылки:", reply_markup=markup)
#     else:
#         await message.answer("У вас нет прав доступа к админ панели.")
#
#
# async def generate_link_easy_access(message: types.Message):
#     if user_exists(message.from_user.id) and get_user_role(message.from_user.id) == 'admin':
#         link = generate_unique_code()
#         user_links_access[link] = 'EasyTask'
#
#         markup = ReplyKeyboardMarkup(resize_keyboard=True)
#         markup.add(KeyboardButton('В главное меню'))
#
#         await message.answer(f"Ссылка на доступ к Easy\-Task: `{link}`", parse_mode='markdownv2', reply_markup=markup)
#     else:
#         await message.answer("У вас нет прав доступа к админ панели.")


def register_admin_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(grant_admin, lambda message: message.text == '/UnyLyZZBiWlLcaSvyRWw')
    dp.register_message_handler(admin_panel, lambda message: message.text == 'Админ панель')
    dp.register_message_handler(wow_task_coins, lambda message: message.text == 'Монеты для Wow-Task')
    dp.register_message_handler(generate_link_wow_500,
                                lambda message: message.text == 'Сгенерировать ссылку на 500 монет')
    dp.register_message_handler(generate_link_wow_600,
                                lambda message: message.text == 'Сгенерировать ссылку на 600 монет')
    dp.register_message_handler(generate_link_wow_700,
                                lambda message: message.text == 'Сгенерировать ссылку на 700 монет')
    dp.register_message_handler(easy_task_coins, lambda message: message.text == 'Монеты для Easy-Task')
    dp.register_message_handler(generate_link_easy_300,
                                lambda message: message.text == 'Сгенерировать ссылку на 300 монет')
    dp.register_message_handler(generate_link_easy_200,
                                lambda message: message.text == 'Сгенерировать ссылку на 200 монет')
    dp.register_message_handler(generate_link_easy_50,
                                lambda message: message.text == 'Сгенерировать ссылку на 50 монет')
    # dp.register_message_handler(urls_access, lambda message: message.text == 'Ссылки для доступа')
    # dp.register_message_handler(generate_link_easy_access,
    #                             lambda message: message.text == 'Сгенерировать ссылку на доступ к Easy-Task')
