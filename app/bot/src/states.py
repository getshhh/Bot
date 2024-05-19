from aiogram.dispatcher.filters.state import State, StatesGroup


class NameStateInstance(StatesGroup):
    waiting_for_name_name: State = State()
    confirm_name: State = State()
    waiting_for_confirm: State = State()


class WowTaskState(StatesGroup):
    waiting_for_moder = State()
    waiting_for_deadline = State()
    waiting_for_task = State()
    waiting_for_coins_amount = State()
    asking_for_media = State()
    waiting_for_media = State()


class EasyState(StatesGroup):
    waiting_for_moder_easy1: State = State()
    waiting_for_deadline_easy1: State = State()
    waiting_for_task_easy1: State = State()
    waiting_for_coins_amount_easy1: State = State()
    asking_for_media_easy1: State = State()
    waiting_for_media_easy1 = State()


class EasyState2(StatesGroup):
    waiting_for_moder_easy2 = State()
    waiting_for_deadline_easy2 = State()
    waiting_for_task_easy2 = State()
    waiting_for_coins_amount_easy2 = State()
    asking_for_media_easy2 = State()
    waiting_for_media_easy2 = State()


class EasyState3(StatesGroup):
    waiting_for_moder_easy3 = State()
    waiting_for_deadline_easy3 = State()
    waiting_for_task_easy3 = State()
    waiting_for_coins_amount_easy3 = State()
    asking_for_media_easy3 = State()
    waiting_for_media_easy3 = State()

#
# name_state_instance = NameStateInstance()
