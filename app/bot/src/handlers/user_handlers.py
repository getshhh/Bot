import re

from aiogram import types, Dispatcher
import logging

from aiogram.dispatcher import FSMContext, filters
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.database.database_func import save_user, get_is_admin, user_exists, get_user_balance
from src.keyboards.main_keyboards import create_main_kb, create_task_kb
from src.states import NameStateInstance
from src.variables import user_links, user_balances, user_names

logger = logging.getLogger(__name__)


async def send_welcome(message: types.Message):
    markup = create_main_kb(get_is_admin(message.from_user.id))
    if user_exists(message.from_user.id):
        await message.answer("С возвращением!", reply_markup=markup)
    else:
        await message.answer("Привет! Как тебя зовут?", reply_markup=markup)
        await NameStateInstance.confirm_name.set()


async def confirm_name(message: types.Message, state: FSMContext):
    if re.fullmatch('[А-ЯЁ][а-яё]+\s+[А-ЯЁ][а-яё]+', message.text):
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(*[InlineKeyboardButton('Всё верно', callback_data='confirm_name'),
                     InlineKeyboardButton('Изменить', callback_data='change_name')])
        await state.update_data(user_name=message.text)
        await NameStateInstance.waiting_for_confirm.set()
        await message.answer(f'Вас зовут *{message.text}*?', reply_markup=markup, parse_mode='markdown')


    else:
        await message.answer('Введите имя и фамилию в правильном формате. Например: Иван Иванов')


async def save_name(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    name = user_data.get('user_name')
    if name and isinstance(name, str):
        await callback.message.answer(f"Добро пожаловать, {name}!")
        await callback.answer()
        try:
            await callback.message.delete()
        except:
            pass
        save_user(callback.from_user.id, name)
        user_names[callback.from_user.id] = name
        await state.finish()
    else:
        await callback.message.answer('Как тебя зовут?')
        await NameStateInstance.confirm_name.set()


async def change_name(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer('Как тебя зовут?')
    try:
        await callback.message.delete()
    except:
        pass
    await NameStateInstance.confirm_name.set()
    await callback.answer()


# async def handle_name(message: types.Message, state: FSMContext):
#     name = message.text
#
#     if user_exists(message.from_user.id):
#         await message.answer("Вы уже зарегистрированы!")
#     else:
#         await message.answer(f"Добро пожаловать, {name}!")
#         save_user(message.from_user.id, name)
#         user_names[message.from_user.id] = name
#
#     await state.finish()


async def go_back(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        user_id = data.get('user_id')

    markup = create_main_kb(get_is_admin(user_id))

    await message.answer("Вы вернулись в главное меню", reply_markup=markup)
    await state.finish()


async def back_to_main_menu(message: types.Message):
    markup = create_main_kb(get_is_admin(message.from_user.id))

    await message.answer("Главное меню:", reply_markup=markup)


async def send_tasks(message: types.Message):
    markup = create_task_kb()
    await message.answer("Выберите задание:", reply_markup=markup)


async def check_balance(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.full_name

    if user_id in user_balances:
        balance = user_balances[user_id]
        await message.answer(f"{user_name}, ваш текущий баланс: {balance}")
    else:
        result = get_user_balance(user_id)

        if result:
            balance = result[0]
            user_balances[user_id] = balance
            await message.answer(f"{user_name}, ваш текущий баланс: {balance}")
        else:
            await message.answer("Баланс не установлен.")


async def process_link_wow(message: types.Message):
    user_id = message.from_user.id
    link = message.text
    if link in user_links:
        coins = user_links[link]
        user_balances[user_id] = user_balances.get(user_id, 0) + coins

        save_user(user_id, message.from_user.full_name, user_balances[user_id])

        await message.answer("Монеты начислены")
        del user_links[link]
    else:
        await message.answer("Недействительная ссылка.")


async def process_link_easy(message: types.Message):
    user_id = message.from_user.id
    link = message.text
    if link in user_links:
        coins = user_links[link]
        user_balances[user_id] = user_balances.get(user_id, 0) + coins

        save_user(user_id, message.from_user.full_name, user_balances[user_id])

        await message.answer("Монеты начислены")
        del user_links[link]
    else:
        await message.answer("Недействительная ссылка.")


# async def process_link(message: types.Message):
#     user_id = message.from_user.id
#     link = message.text
#     if link in user_links_access:
#         if user_links_access[link] == 'EasyTask':
#
#             access = get_user_access_info(user_id)
#             if access is None:
#                 grant_user_access(user_id, 'EasyTask')
#                 await message.answer("Доступ разрешен")
#                 del user_links_access[link]
#             else:
#                 await message.answer("У вас уже есть доступ к EasyTask")
#
#         else:
#             await message.answer("Недействительная ссылка.")
#     else:
#         await message.answer("Недействительная ссылка.")


async def show_profile(message: types.Message):
    user_id = message.from_user.id
    user_name = user_names.get(user_id, message.from_user.full_name)

    await message.answer(f"Имя: {user_name}\nID: {user_id}")


async def echo_handler(message: types.Message):
    await message.answer('Неизвестная команда', reply_markup=create_main_kb(get_is_admin(message.from_user.id)))


def register_user_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(send_welcome, commands=['start'])
    # dp.register_message_handler(handle_name, state=NameStateInstance.waiting_for_name_name)
    dp.register_message_handler(confirm_name, state=NameStateInstance.confirm_name)
    dp.register_callback_query_handler(save_name, lambda c: c.data and c.data == 'confirm_name',
                                       state=NameStateInstance.waiting_for_confirm)
    dp.register_callback_query_handler(change_name, lambda c: c.data and c.data == 'change_name',
                                       state=NameStateInstance.waiting_for_confirm)
    dp.register_message_handler(go_back, lambda message: message.text == 'в главное меню', state='*')
    dp.register_message_handler(back_to_main_menu, filters.Text(equals='В главное меню'))
    dp.register_message_handler(send_tasks, lambda message: message.text == 'Задания')
    dp.register_message_handler(check_balance, lambda message: message.text == 'Баланс')
    dp.register_message_handler(process_link_wow, lambda message: message.text in user_links.keys())
    dp.register_message_handler(process_link_easy, lambda message: message.text in user_links.keys())
    # dp.register_message_handler(process_link, lambda message: message.text in user_links_access.keys())
    dp.register_message_handler(show_profile, lambda message: message.text == 'Профиль')
    dp.register_message_handler(echo_handler)
