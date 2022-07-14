import asyncio
from loader import dp, bot
from filters import UserRoleFilter, CheckInputDataFilter
from states import FindState, LikeState
from time import time
from keyboards.default import cancel_search_keyboard, main_menu_keboard, return_to_find_keyboard
from keyboards.inline import reaction_keyboard, show_likes_keyboard, lite_reaction_keyboard
from utils.db import update_user, get_city, get_users, create_like, get_like, delete_like
from utils.geo import sort_distance_cities
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery


@dp.message_handler(UserRoleFilter(role="user"), lambda message: message.text.lower() == "искать")
async def start_find(message: Message, user_info, state: FSMContext):
    if (user_info['check_time'] is None) or (user_info['check_time'] - int(time()) > 86400):
        await update_user(message.from_user.id, checked=[message.from_user.id], check_time=int(time()))
        user_info = await get_users(one=True, telegram_id=message.from_user.id)
    user_city = await get_city(id=user_info['city_id'])
    cities = await get_city(all=True)
    sorted_cities =  sort_distance_cities(cities, user_city)
    await FindState.inSearch.set()
    async with state.proxy() as data:
        data['cities'] = sorted_cities
    await message.answer("Начинаю поиск", reply_markup=cancel_search_keyboard)
    await find(message, state, user_info)


@dp.message_handler(lambda message: message.text.lower() == "закончить поиск", state=[FindState.inSearch, FindState.reaction])
async def cancel_search(message: Message, state: FSMContext):
    await asyncio.sleep(1)
    try:
        async with state.proxy() as data:
            await data['msg'].delete()
            await data['msg2'].delete()
    except:
        pass
    await state.finish()
    await message.answer("Поиск окончен", reply_markup=main_menu_keboard)



async def find(message: Message, state: FSMContext, user_info):
    find_sex = user_info['find_sex']
    find_sex = [i for i in find_sex]
    data = await state.get_data()
    cities = data['cities']
    for city in cities:
        required_user = await get_users(city_id=city['id'], checked=user_info['checked'], find_sex=find_sex)
        if required_user is None:
            continue
        else:
            await FindState.reaction.set()
            text = f"{required_user['name']}, {required_user['age']}, {city['name']}"
            if not (required_user['description'] is None):
                text += f" - {required_user['description']}"
            async with state.proxy() as data:
                data['required_user'] = {'telegram_id': required_user['telegram_id']}
                if not (required_user['photo_id'] is None):
                    data['msg'] = await message.answer_photo(required_user['photo_id'])
                else:
                    data['msg'] = await message.answer_video(required_user['video_id'])
                data['msg2'] = await message.answer(text, reply_markup=reaction_keyboard)
            return
    await state.finish()
    await message.answer("Увы, больше никого не могу найти", reply_markup=main_menu_keboard)


@dp.callback_query_handler(lambda callback: callback.data.startswith('reaction'), state=FindState.reaction)
async def reaction(callback: CallbackQuery, state: FSMContext, user_info):
    checked = user_info['checked']
    async with state.proxy() as data:
        try:
            recipient_id = data['required_user']['telegram_id']
            checked.append(recipient_id)
        except:
            return
        try:
            await data['msg'].delete()
            await data['msg2'].delete()
        except:
            pass
    reaction = callback.data.replace("reaction_", "")
    if reaction == "dislike":
        await update_user(telegram_id=callback.from_user.id, checked=checked)
        user_info = await get_users(one=True, telegram_id=callback.from_user.id)
        await find(callback.message, state, user_info)
    elif reaction == "like":
        await update_user(telegram_id=callback.from_user.id, checked=checked)
        user_info = await get_users(one=True, telegram_id=callback.from_user.id)
        await create_like(sender=callback.from_user.id, recipient=recipient_id)
        await bot.send_message(recipient_id, "Вы кому то понравились, показать?\n(Для просмотра нужно завершить поиск и заполнение всех анкет)", reply_markup=show_likes_keyboard)
        await find(callback.message, state, user_info)
    else:
        await FindState.text.set()
        await callback.message.answer("Введите желаемый текст который хотите отправить пользователю", reply_markup=return_to_find_keyboard)


@dp.message_handler(lambda message: message.text.lower() == "вернуться обратно", state=FindState.text)
async def return_to_find(message: Message, state: FSMContext, user_info):
    await find(message, state, user_info)


@dp.message_handler(CheckInputDataFilter(data_type='description'), state=FindState.text)
async def reaction_message(message: Message, state: FSMContext, user_info):
    checked = user_info['checked']
    async with state.proxy() as data:
        try:
            recipient_id = data['required_user']['telegram_id']
            checked.append(recipient_id)
        except:
            return
    await update_user(telegram_id=message.from_user.id, checked=checked)
    await create_like(sender=message.from_user.id, recipient=recipient_id, description=message.text)
    user_info = await get_users(one=True, telegram_id=message.from_user.id)
    await bot.send_message(recipient_id, "Вы кому то понравились, показать?\n(Для просмотра нужно завершить поиск и заполнение всех анкет)", reply_markup=show_likes_keyboard)
    await message.answer("Сообщение отправленно")
    await find(message, state, user_info)



@dp.callback_query_handler(text="show_likes")
async def show_likes(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    like = await get_like(callback.from_user.id)
    if like is None:
        await callback.message.answer("Больше нету симпатий")
        try:
            await state.finish()
        except:
            pass
        return
    sender = await get_users(one=True, telegram_id=like['sender'])
    sender_city = await get_city(id=sender['city_id'])
    text = f"{sender['name']}, {sender['age']}, {sender_city['name']}"
    if not (sender['description'] is None):
        text += f" - {sender['description']}"
    if not (like['description'] is None):
        text += f"\n💌 Сообщение для тебя: {like['description']}"
    async with state.proxy() as data:
        data['sender'] = {'telegram_id': sender['telegram_id'], 'username': sender['username']}
        if not (sender['photo_id'] is None):
            data['msg'] = await callback.message.answer_photo(sender['photo_id'])
        else:
            data['msg'] = await callback.message.answer_video(sender['video_id'])
        data['msg2'] = await callback.message.answer(text, reply_markup=lite_reaction_keyboard)
        data['like_id'] = like['id']
    await LikeState.reaction.set()


@dp.callback_query_handler(lambda callback: callback.data.startswith('reaction'), state=LikeState.reaction)
async def like_reaction(callback: CallbackQuery, state: FSMContext, user_info):
    async with state.proxy() as data:
        try:
            await data['msg'].delete()
            await data['msg2'].delete()
        except:
            pass
        reaction = callback.data.replace("reaction_", "")
        if reaction == "like":
            await callback.message.answer(f"Отлично, приятного общения @{data['sender']['username']}")
            user_city = await get_city(id=user_info['city_id'])
            text = f"{user_info['name']}, {user_info['age']}, {user_city['name']}"
            if not (user_info['description'] is None):
                text += f" - {user_info['description']}"
            await bot.send_message(data['sender']['telegram_id'], "Взаимная симпатия")
            if not (user_info['photo_id'] is None):
                await bot.send_photo(data['sender']['telegram_id'], user_info['photo_id'])
            else:
                await bot.send_video(data['sender']['telegram_id'], user_info['video_id'])
            await bot.send_message(data['sender']['telegram_id'], text)
            await bot.send_message(data['sender']['telegram_id'], f"Приятного общения @{user_info['username']}")
        await delete_like(id=data['like_id'])
        checked = user_info['checked']
        try:
            checked.append(data['sender']['telegram_id'])
            await update_user(callback.from_user.id, checked=checked)
        except:
            checked = [callback.from_user.id, data['sender'], ['telegram_id']]
            check_time = time()
            await update_user(callback.from_user.id, checked=checked, check_time=check_time)
    await show_likes(callback, state)








@dp.message_handler(UserRoleFilter(role="user"))
async def unknown_command(message: Message):
    await message.answer("Охх... к сожалению, я не могу понять вас", reply_markup=main_menu_keboard)