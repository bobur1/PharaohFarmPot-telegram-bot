from aiogram.types import Message, CallbackQuery
from tg_bot.data.database import add_user_start
from tg_bot.data.loader import dp
from tg_bot.keyboards.user.inline import choice_start


@dp.message_handler(commands=['start'])
async def main_start(message: Message):
    await message.delete()
    user_id = message.chat.id
    user_name = message.chat.first_name
    add_user_start(user_id, user_name)
    await message.answer(text=f'Welcome <b>{message.chat.first_name}</b> to the Pharaoh Farm Pot Bot!💰\n\nBelow you '
                              f'can see the <code><b>❗ Info</b></code> of our project\n\n\n<u>To find out what this bot can do, '
                              f'follow the /help command</u>', reply_markup=choice_start())


@dp.callback_query_handler(text_startswith='next')
async def next_start(call: CallbackQuery):
    await call.message.edit_text(
        text=f'Welcome <b>{call.message.chat.first_name}</b> to the Pharaoh Farm Pot Bot!💰\n\nBelow you '
             f'can see the <code><b>❗ Info</b></code> of our project\n\n\n<u>To find out what this bot can do, '
             f'follow the /help command</u>', reply_markup=choice_start())
