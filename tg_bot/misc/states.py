from aiogram.dispatcher.filters.state import StatesGroup, State


class Mailing(StatesGroup):
    text = State()
    state = State()
    channel = State()
    channel_media = State()
    photo = State()
    video = State()


class AddWalletUser(StatesGroup):
    text = State()
    wallet_state = State()
