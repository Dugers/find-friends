from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Message, CallbackQuery, Update
from utils.db import get_users, update_user


class UserRoleMiddleware(BaseMiddleware):
    async def on_pre_process_message(self, message: Message, data):
        data['user_info'] = await get_users(one=True, telegram_id=message.from_user.id)
        try:
            if data['user_info']['username'] != message.from_user.username:
                await update_user(message.from_user.id, username=message.from_user.username)
        except:
            pass

    async def on_pre_process_callback_query(self, callback: CallbackQuery, data):
        data['user_info'] = await get_users(one=True, telegram_id=callback.from_user.id)
        try:
            if data['user_info']['username'] != callback.from_user.username:
                await update_user(callback.from_user.id, username=callback.from_user.username)
        except:
            pass