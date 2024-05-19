import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from src.func import initialize_logger
from src.handlers.admin_handlers import register_admin_handlers
from src.settings import API_TOKEN

# handlers
from src.handlers.easy_task2_handlers import register_easy_task2_handlers
from src.handlers.easy_task3_handlers import register_easy_task3_handlers
from src.handlers.easy_task_handlers import register_easy_task_handlers
from src.handlers.user_handlers import register_user_handlers
from src.handlers.wow_task_handlers import register_wow_task_handlers

initialize_logger()


def register_all_handlers(dp: Dispatcher) -> None:
    register_admin_handlers(dp)
    register_wow_task_handlers(dp)
    register_easy_task_handlers(dp)
    register_easy_task2_handlers(dp)
    register_easy_task3_handlers(dp)
    register_user_handlers(dp)


async def main() -> None:
    bot = Bot(API_TOKEN)

    dp = Dispatcher(bot, storage=MemoryStorage())

    register_all_handlers(dp)

    try:
        await dp.start_polling()
    except Exception as err:
        logging.error(f'Ошибка main(): {err}')


if __name__ == '__main__':
    asyncio.run(main())
