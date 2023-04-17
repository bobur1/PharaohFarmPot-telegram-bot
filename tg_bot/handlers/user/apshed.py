from aiogram import Bot

from tg_bot.data.database import get_wallet_user
from tg_bot.utils.read_contract import double_up, doubling_amount


async def double_up_alert_users(bot: Bot, chat_id: int):
    # if not double_up(chat_id):
    #     doubling = doubling_amount(chat_id)
    #     user_wallet = get_wallet_user(chat_id)
    #     await bot.send_message(chat_id=chat_id, text=f'<b>❗ATTENTION!!! DOUBLE UP REQUIRED❗</b>\n\nWallet: <a href="https://bscscan.com/address/{user_wallet}">{user_wallet[0:6]}...{user_wallet[36:43]}</a>\nAmount required for Double Up: {float(doubling):.2f} CAF', disable_web_page_preview=True)
    # else:
    #     pass
    pass

async def new_member_notification(bot: Bot, chat_id: int, member_wallet: str, member_token_amount: int, lvl: str):
    user_wallet = get_wallet_user(chat_id)
    await bot.send_message(chat_id=chat_id, text=f'<b>TEAM MEMBER DEPOSIT!!!💰</b>\n\nWallet: <a href="https://bscscan.com/address/{member_wallet}">{member_wallet[0:6]}...{member_wallet[36:43]}</a>\nAmount: {float(member_token_amount):.2f} CAF\n ', disable_web_page_preview=True)

