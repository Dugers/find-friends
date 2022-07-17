from utils.db import get_users, update_user
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.handler import CancelHandler


class UserRoleMiddleware(BaseMiddleware):
    async def on_pre_process_message(self, message: Message, data):
        if message.from_user.username is None:
            await message.answer("Для использования бота вам нужно иметь username в телеграм\nДля этого зайдите в настройки -> \"Изменить профиль\" -> \"Имя пользователя\"\nЗатем запишите туда любое имя")
            raise CancelHandler()
        data['user_info'] = await get_users(one=True, telegram_id=message.from_user.id)
        try:
            if data['user_info']['username'] != message.from_user.username:
                await update_user(message.from_user.id, username=message.from_user.username)
        except:
            pass

    async def on_pre_process_callback_query(self, callback: CallbackQuery, data):
        if callback.from_user.username is None:
            await callback.message.answer("Для использования бота вам нужно иметь username в телеграм\nДля этого зайдите в настройки -> \"Изменить профиль\" -> \"Имя пользователя\"\nЗатем запишите туда любое имя")
            raise CancelHandler()
        data['user_info'] = await get_users(one=True, telegram_id=callback.from_user.id)
        try:
            if data['user_info']['username'] != callback.from_user.username:
                await update_user(callback.from_user.id, username=callback.from_user.username)
        except:
            pass