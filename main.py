from aiogram import executor
from data import ADMIN_ID, WEBHOOK_PATH, WEBAPP_HOST, WEBAPP_PORT, WEBHOOK_URL
from loader import bot
from handlers import dp
from middlewares import setup_middlewares
from filters import setup_filters
from utils.db import create_tables


async def on_startup(dp):
    setup_middlewares(dp)
    setup_filters(dp)
    await create_tables()
    await bot.send_message(ADMIN_ID, "Bot started working")
    # await bot.set_webhook(WEBHOOK_URL)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
    # executor.start_webhook(
    #     dispatcher=dp,
    #     webhook_path=WEBHOOK_PATH,
    #     skip_updates=True,
    #     on_startup=on_startup,
    #     host=WEBAPP_HOST,
    #     port=WEBAPP_PORT
    # )