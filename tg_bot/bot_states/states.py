from aiogram.fsm.state import StatesGroup, State


class States(StatesGroup):
    PHONE_STATE = State()
    GEO_STATE = State()
    MENU_STATE = State()
    ADMIN_STATE = State()
    ADMIN_UNBLOCK_STATE = State()





