from aiogram import executor, Dispatcher
from tg_bot.handlers.user import dp as users
from tg_bot.misc.commands import set_commands, remove_commands
from tg_bot.middlewares.alert_double_up import DoubleUp
from tg_bot.data.loader import dp
from tg_bot.data.loader import scheduler


# Выполнение функции после запуска бота
async def on_startup(dp: Dispatcher):
    await set_commands(dp)
    await dp.bot.delete_webhook()
    await dp.bot.get_updates(offset=-1)
    print('Start bot!')


# Выполнение функции после выключения бота
async def on_shutdown(dp: Dispatcher):
    await remove_commands(dp)
    await dp.storage.close()
    await dp.storage.wait_closed()
    await (await dp.bot.get_session()).close()
    print('Stop bot!')

if __name__ == "__main__":
    dp.middleware.setup(DoubleUp())
    scheduler.start()

    executor.start_polling(users, on_startup=on_startup, on_shutdown=on_shutdown, skip_updates=True)