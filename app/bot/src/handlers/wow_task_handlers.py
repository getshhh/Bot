from datetime import datetime

from aiogram import types, Dispatcher

from aiogram.dispatcher import FSMContext, filters

from src.database.database_func import save_wow_task, get_wow_task_info
from src.states import WowTaskState


async def show_wow_task(message: types.Message):
    wow_task_info = get_wow_task_info()
    if wow_task_info:
        deadline, wow_task_text, coins, owner, media = wow_task_info
        current_time = datetime.now()

        # Предполагается, что deadline из базы данных представляет собой строку
        deadline = datetime.strptime(deadline, '%d %B %Y, %H:%M')

        if current_time <= deadline:
            if media:
                await message.answer_photo(media,
                                           caption=f"Дедлайн: {deadline.strftime('%d %B %Y, %H:%M')}\n\nТекст задания: {wow_task_text}\n\nЦена за задания: {coins}\n\nМодератор для проверки задания: {owner}")
            else:
                await message.answer(
                    f"Дедлайн: {deadline.strftime('%d %B %Y, %H:%M')}\n\nТекст задания: {wow_task_text}\n\nЦена за задания: {coins}\n\nМодератор для проверки задания: {owner}")
        else:
            await message.answer(
                f"Дедлайн: {deadline.strftime('%d %B %Y, %H:%M')}\n\nТекст задания: {wow_task_text}\n\nЦена за задания: {coins}")
    else:
        await message.answer("Задание Wow-Task еще не установлено.")


async def add_wow_task(message: types.Message):
    await message.answer("Введите @ник админа Wow-Task:")
    await WowTaskState.waiting_for_moder.set()


async def handle_name(message: types.Message, state: FSMContext):
    owner = message.text
    if owner.startswith('@'):
        await state.update_data(owner=owner)
        await message.answer("Введите дд-мм-гггг чч:мм для дедлайна Wow-Task:")
        await WowTaskState.waiting_for_deadline.set()
    else:
        await message.answer("Имя админа должно начинаться с символа '@'. Пожалуйста, введите корректное имя.")


async def handle_deadline(message: types.Message, state: FSMContext):
    deadline_input = message.text
    try:
        deadline_datetime = datetime.strptime(deadline_input, '%d-%m-%Y %H:%M')
        deadline = deadline_datetime.strftime('%d %B %Y, %H:%M')
        await state.update_data(deadline=deadline)
        await message.answer("Введите текст задания для Wow-Task:")
        await WowTaskState.waiting_for_task.set()
    except ValueError:
        await message.answer(
            "Неправильный формат даты и времени. Пожалуйста, введите дату в формате 'дд-мм-гггг чч:мм'. Например, '27-02-2024 14:30'")


async def handle_task(message: types.Message, state: FSMContext):
    task_text = message.text
    await message.answer("Введите количество монет в числовом формате:")
    await WowTaskState.waiting_for_coins_amount.set()
    await state.update_data(task_text=task_text)


async def handle_coins_amount(message: types.Message, state: FSMContext):
    coins_amount = message.text
    if coins_amount and coins_amount.isdigit():
        await message.answer("Хотите добавить фото или ссылку на видео? (да/нет)")
        await WowTaskState.asking_for_media.set()
        await state.update_data(coins_amount=coins_amount)
    else:
        await message.answer("Количество монет должно быть числом!")


async def handle_media_decision(message: types.Message, state: FSMContext):
    decision = message.text.lower()
    if decision == 'да':
        await message.answer("Пожалуйста, отправьте фото или ссылку на видео.")
        await WowTaskState.waiting_for_media.set()
    elif decision == 'нет':
        data = await state.get_data()
        deadline = data.get('deadline')
        task_text = data.get('task_text')
        coins_amount = data.get('coins_amount')
        owner = data.get('owner')

        save_wow_task(deadline, task_text, coins_amount, owner, media=None)
        await message.answer("Wow-Task успешно добавлен!")
        await state.finish()
    else:
        await message.answer("Пожалуйста, выберите 'да' или 'нет'.")


async def handle_media(message: types.Message, state: FSMContext):
    media_file_id = message.photo[-1].file_id if message.photo else message.video.file_id

    data = await state.get_data()
    deadline = data.get('deadline')
    task_text = data.get('task_text')
    coins_amount = data.get('coins_amount')
    owner = data.get('owner')

    save_wow_task(deadline, task_text, coins_amount, owner, media=media_file_id)
    await message.answer("Wow-Task успешно добавлен с медиа!")
    await state.finish()


def register_wow_task_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(show_wow_task, filters.Text(equals='Wow-Task'))
    dp.register_message_handler(add_wow_task, commands=['addwow'])
    dp.register_message_handler(handle_name, state=WowTaskState.waiting_for_moder)
    dp.register_message_handler(handle_deadline, state=WowTaskState.waiting_for_deadline)
    dp.register_message_handler(handle_task, state=WowTaskState.waiting_for_task)
    dp.register_message_handler(handle_coins_amount, state=WowTaskState.waiting_for_coins_amount)
    dp.register_message_handler(handle_media_decision, state=WowTaskState.asking_for_media)
    dp.register_message_handler(handle_media, state=WowTaskState.waiting_for_media,
                                content_types=['photo', 'video'])
