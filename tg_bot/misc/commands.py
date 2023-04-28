from aiogram import Dispatcher
from aiogram.types import BotCommand, BotCommandScopeChat, BotCommandScopeDefault

# Команды для юзеров
user_commands = [
    BotCommand("start", "♻ Start and restart the bot"),
    BotCommand("register_wallet", "📃 Register your Account wallet"),
    BotCommand("stats", "👀 Check your Pharaoh Farm Pot Stats of your registered wallet"),
    BotCommand("netdeposit", "👀 Check Pharaoh Farm Pot net deposit of the contract"),
    BotCommand("help", "❓ Learn about the bot's functions")
]


# Установка команд
async def set_commands(dp: Dispatcher):
    await dp.bot.set_my_commands(user_commands, scope=BotCommandScopeDefault())


# Удаление команд
async def remove_commands(dp: Dispatcher):
    await dp.bot.delete_my_commands(scope=BotCommandScopeDefault())
