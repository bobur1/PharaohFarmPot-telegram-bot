from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from tg_bot.data.config import info_message


def choice_start():
    keyboard = InlineKeyboardMarkup(row_width=2,
                                    inline_keyboard=[
                                        [
                                            InlineKeyboardButton(text="👤 Account", callback_data="check_account")
                                        ],
                                        [
                                            InlineKeyboardButton(text="❗ Info", callback_data="info")
                                        ]
                                    ])
    return keyboard


def choice_next():
    keyboard = InlineKeyboardMarkup(row_width=2,
                                    inline_keyboard=[
                                        [
                                            InlineKeyboardButton(text="🚪 Next", callback_data="next")
                                        ]
                                    ])
    return keyboard


# pages set
info_callback = CallbackData("Info", "page")
info = info_message()


def get_choice_info(page: int = 0) -> InlineKeyboardMarkup:
    has_next_page = len(info) > page + 1
    keyboard = InlineKeyboardMarkup(row_width=2,
                                    inline_keyboard=[
                                        [
                                            InlineKeyboardButton(text="⬅",
                                                                 callback_data=info_callback.new(page=page - 1)),
                                            InlineKeyboardButton(text=f"| {page + 1}/8 |",
                                                                 callback_data="dont_click_me"),
                                            InlineKeyboardButton(text="➡",
                                                                 callback_data=info_callback.new(page=page + 1))
                                        ],
                                        [
                                            InlineKeyboardButton(text="🚪 Next", callback_data="next")
                                        ]
                                    ])
    return keyboard


def get_choice_wallet():
    keyboard = InlineKeyboardMarkup(row_width=2,
                                    inline_keyboard=[
                                        [
                                            InlineKeyboardButton(text="✅ Done", callback_data="done_wallet_add_user"),
                                            InlineKeyboardButton(text="❌ Cancel", callback_data="exit_states")
                                        ]
                                    ])
    return keyboard


def get_choice_wallet_cancel():
    keyboard = InlineKeyboardMarkup(row_width=2,
                                    inline_keyboard=[
                                        [
                                            InlineKeyboardButton(text="❌ Cancel", callback_data="exit_states")
                                        ]
                                    ])
    return keyboard
