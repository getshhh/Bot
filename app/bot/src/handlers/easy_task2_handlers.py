from datetime import datetime

from aiogram import types, Dispatcher
import logging

from aiogram.dispatcher import filters, FSMContext
from src.database.database_func import get_easy_task_info2, save_easy_task2

from src.states import EasyState2


async def show_easy_task2(message: types.Message):
    easy_task_info2 = get_easy_task_info2()
    if easy_task_info2:
        deadline, easy_task_text, coins, owner, media = easy_task_info2
        current_time = datetime.now()

        # Предполагается, что deadline из базы данных представляет собой строку
        deadline = datetime.strptime(deadline, '%d %B %Y, %H:%M')

        if current_time <= deadline:
            if media:
                await message.answer_photo(media,
                                           caption=f"Дедлайн: {deadline.strftime('%d %B %Y, %H:%M')}\n\nТекст задания: {easy_task_text}\n\nЦена за задания: {coins}\n\nМодератор для проверки задания: {owner}")
            else:
                await message.answer(
                    f"Дедлайн: {deadline.strftime('%d %B %Y, %H:%M')}\n\nТекст задания: {easy_task_text}\n\nЦена за задания: {coins}\n\nМодератор для проверки задания: {owner}")
        else:
            await message.answer(
                f"Дедлайн: {deadline.strftime('%d %B %Y, %H:%M')}\n\nТекст задания: {easy_task_text}\n\nЦена за задания: {coins}")
    else:
        await message.answer("Задание Easy-Task 2 еще не установлено.")


async def add_easy_task2(message: types.Message):
    await message.answer("Введите @ник администратора Easy-Task 2:")
    await EasyState2.waiting_for_moder_easy2.set()


async def handle_name_easy2(message: types.Message, state: FSMContext):
    owner_easy2 = message.text
    if owner_easy2.startswith('@'):
        await state.update_data(owner_easy2=owner_easy2)
        await message.answer("Введите дд-мм-гггг чч:мм для дедлайна Easy-Task 2:")
        await EasyState2.waiting_for_deadline_easy2.set()
    else:
        await message.answer("Имя администратора должно начинаться с символа '@'. Пожалуйста, введите корректное имя.")


async def handle_deadline_easy2(message: types.Message, state: FSMContext):
    deadline_input = message.text
    try:
        deadline_datetime = datetime.strptime(deadline_input, '%d-%m-%Y %H:%M')
        deadline = deadline_datetime.strftime('%d %B %Y, %H:%M')
        await state.update_data(deadline=deadline)
        await message.answer("Введите текст задания для Easy-Task 2:")
        await EasyState2.waiting_for_task_easy2.set()
    except ValueError:
        await message.answer(
            "Неправильный формат даты и времени. Пожалуйста, введите дату в формате 'дд-мм-гггг чч:мм'. Например, '27-02-2024 14:30'")


async def handle_task_easy2(message: types.Message, state: FSMContext):
    task_text_easy2 = message.text
    await message.answer("Введите количество монет в числовом формате:")
    await EasyState2.waiting_for_coins_amount_easy2.set()
    await state.update_data(task_text_easy2=task_text_easy2)


async def handle_coins_amount_easy2(message: types.Message, state: FSMContext):
    coins_amount_easy2 = message.text
    if coins_amount_easy2 and coins_amount_easy2.isdigit():
        await message.answer("Хотите добавить фото или ссылку на видео? (да/нет)")
        await EasyState2.asking_for_media_easy2.set()
        await state.update_data(coins_amount_easy2=coins_amount_easy2)
    else:
        await message.answer("Количество монет должно быть числом!")


async def handle_media_decision_easy2(message: types.Message, state: FSMContext):
    decision_easy2 = message.text.lower()
    if decision_easy2 == 'да':
        await message.answer("Пожалуйста, отправьте фото или ссылку на видео.")
        await EasyState2.waiting_for_media_easy2.set()
    elif decision_easy2 == 'нет':
        data = await state.get_data()
        deadline_easy2 = data.get('deadline')
        task_text_easy2 = data.get('task_text_easy2')
        coins_amount_easy2 = data.get('coins_amount_easy2')
        owner_easy2 = data.get('owner_easy2')

        save_easy_task2(deadline_easy2, task_text_easy2, coins_amount_easy2, owner_easy2, media=None)
        await message.answer("Easy-Task 2 успешно добавлен!")
        await state.finish()
    else:
        await message.answer("Пожалуйста, выберите 'да' или 'нет'.")


async def handle_media_easy2(message: types.Message, state: FSMContext):
    media_file_id = message.photo[-1].file_id if message.photo else message.video.file_id

    data = await state.get_data()
    deadline_easy2 = data.get('deadline')
    task_text_easy2 = data.get('task_text_easy2')
    coins_amount_easy2 = data.get('coins_amount_easy2')
    owner_easy2 = data.get('owner_easy2')

    save_easy_task2(deadline_easy2, task_text_easy2, coins_amount_easy2, owner_easy2, media=media_file_id)
    await message.answer("Easy-Task 2 успешно добавлен с медиа!")
    await state.finish()


def register_easy_task2_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(show_easy_task2, filters.Text(equals='Easy-Task 2'))
    dp.register_message_handler(add_easy_task2, commands=['addeasy2'])
    dp.register_message_handler(handle_name_easy2, state=EasyState2.waiting_for_moder_easy2)
    dp.register_message_handler(handle_deadline_easy2, state=EasyState2.waiting_for_deadline_easy2)
    dp.register_message_handler(handle_task_easy2, state=EasyState2.waiting_for_task_easy2)
    dp.register_message_handler(handle_coins_amount_easy2, state=EasyState2.waiting_for_coins_amount_easy2)
    dp.register_message_handler(handle_media_decision_easy2, state=EasyState2.asking_for_media_easy2)
    dp.register_message_handler(handle_media_easy2, state=EasyState2.waiting_for_media_easy2,
                                content_types=['photo', 'video'])
