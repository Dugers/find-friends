from loader import dp
from .profile import user_profile
from states import UserRegistrationState
from filters import UserRoleFilter, CheckInputDataFilter
from utils.geo import get_geowork
from utils.db import create_user, get_city, create_city
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from keyboards.inline import select_sex_keyboard, select_find_sex_keyboard
from keyboards.default import UserUpdateValuesKeyboard, main_menu_keboard


@dp.message_handler(UserRoleFilter(role="new_user"), commands=['start', 'registration'])
async def start(message: Message):
    await message.answer("Привет, я бот для <b>поиска новых друзей</b>")
    await message.answer_sticker("CAACAgIAAxkBAAEFMLhiwwHC9tc-9LEnGjhu2Lp0_wZcAgACRQADeKjmD8U-FA5dAz7LKQQ")
    await UserRegistrationState.name.set()
    await message.answer("Давай создадим твою анкету, отправь мне свое имя")


@dp.message_handler(UserRoleFilter(role="user"), commands=['start', 'registration'])
async def not_start(message: Message):
    await message.answer("Я уже знаю тебя, привет")
    await message.answer_sticker("CAACAgIAAxkBAAEFMLhiwwHC9tc-9LEnGjhu2Lp0_wZcAgACRQADeKjmD8U-FA5dAz7LKQQ")


@dp.message_handler(UserRoleFilter(role="user"), state=UserRegistrationState)
async def check(message: Message):
    await message.answer("Так... стоп... я вспомнил тебя! У тебя уже есть анкета")


@dp.message_handler(CheckInputDataFilter(data_type="name"), state=UserRegistrationState.name)
async def set_name(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await UserRegistrationState.next()
    await message.answer("Отличное имя, давай пойдем дальше")
    await message.answer("Отправь мне свой возраст")


@dp.message_handler(CheckInputDataFilter(data_type="name", invalid=True), state=UserRegistrationState.name)
async def invalid_name(message: Message):
    await message.answer("Имя указано не правильно, возможные причины:\n❌ Слишком короткое (меньше 3 символов) или слишком длинное (больше 30 символов)\n❌ Является числом\n❌ Начинается с / или содержит @")
    await message.answer("Попробуйте снова")


@dp.message_handler(CheckInputDataFilter(data_type="age"), state=UserRegistrationState.age)
async def set_age(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['age'] = int(message.text)
    await UserRegistrationState.next()
    await message.answer("Возраст я зафиксировал, давай продолжим")
    await message.answer("(Используйте кнопки) Выбери свой пол:", reply_markup=select_sex_keyboard)


@dp.message_handler(CheckInputDataFilter(data_type="age", invalid=True), state=UserRegistrationState.age)
async def invalid_name(message: Message):
    await message.answer("Возраст указан не правильно, возможные причины:\n❌ Не является числом\n❌ Больше 100 или меньше 10")
    await message.answer("Попробуйте снова")

@dp.callback_query_handler(lambda callback: callback.data.startswith("sex_"), state=UserRegistrationState.sex)
async def set_sex(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    async with state.proxy() as data:
        data['sex'] = callback.data.replace("sex_", "")
        sex = data['sex']
    if sex == "M":
        await callback.message.edit_text("Пол: Мужской")
    else:
        await callback.message.edit_text("Пол: Женский")

    await UserRegistrationState.next()
    await callback.message.answer("Отлично, твой пол мы записали")
    await callback.message.answer("(Используйте кнопки) Выбери кто тебе интересен:", reply_markup=select_find_sex_keyboard)


@dp.callback_query_handler(lambda callback: callback.data.startswith("find_sex_"), state=UserRegistrationState.find_sex)
async def set_find_sex(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    async with state.proxy() as data:
        data['find_sex'] = callback.data.replace("find_sex_", "")
        data['city_id'] = False
        find_sex = data['find_sex']
    if find_sex == "M":
        await callback.message.edit_text("Искать: Парней")
    elif find_sex == "F":
        await callback.message.edit_text("Искать: Девушек")
    else:
        await callback.message.edit_text("Искать: Всех")
    await UserRegistrationState.next()
    await callback.message.answer("Хороший выбор, давай пойдем дальше")
    await callback.message.answer("Напишите свой город или отправь метку", reply_markup=UserUpdateValuesKeyboard(field_name='city').keyboard)

@dp.message_handler(content_types=['location'], state=UserRegistrationState.city_id)
async def set_city_id_location(message: Message, state):
    coordinates = (message.location.latitude, message.location.longitude)
    city_data = await get_geowork(coordinates=coordinates, need_name=True, need_coordinates=True)
    if city_data:
        async with state.proxy() as data:
            data['city_id'] = city_data
        await UserRegistrationState.next()
        await message.answer("Ура! Мы смогли найти ваш город на карте", reply_markup=ReplyKeyboardRemove())
        await message.answer("Теперь отправьте мне свою фотографию или видео")
    else:
        await message.answer("Технические неполадки, попробуйте позже")

@dp.message_handler(CheckInputDataFilter(data_type="name"), state=UserRegistrationState.city_id)
async def set_city_id_text(message: Message, state: FSMContext):
    async with state.proxy() as data:
        if data['city_id'] == False:
            data['city_id'] = True
        else:
            await message.answer("Проверяем ваш город, подождите")
            return
    await message.answer("Ожидайте (до 30 секунд)")
    city_data = await get_geowork(name=message.text, need_name=True, need_coordinates=True)
    if city_data:
        async with state.proxy() as data:
            data['city_id'] = city_data
        await UserRegistrationState.next()
        await message.answer("Ура! Мы смогли найти ваш город на карте", reply_markup=ReplyKeyboardRemove())
        await message.answer("Теперь отправьте мне свою фотографию или видео")
    else:
        await message.answer("Город указан не верно, попробуйте снова")
        async with state.proxy() as data:
            data['city_id'] = False


@dp.message_handler(CheckInputDataFilter(data_type="name", invalid=True), state=UserRegistrationState.city_id)
async def invalid_city_id_text(message: Message):
    await message.answer("Название города указано не правильно, возможные причины:\n❌ Название слишком длинное или короткое\n❌ Содержит / или @")
    await message.answer("Попробуйте снова")

@dp.message_handler(content_types=['photo', 'video'], state=UserRegistrationState.photo_id)
async def set_photo(message: Message, state: FSMContext):
    await UserRegistrationState.next()
    try:
        photo_id = message.photo[0]['file_id']
        video_id = None
    except:
        video_id = message.video.file_id
        photo_id = None
    async with state.proxy() as data:
        data['photo_id'] = photo_id
        data['video_id'] = video_id
        data['reg_start'] = False
    await message.answer("Готово!")
    await message.answer("Теперь отправь мне свое описание или выбери оставить пустым", reply_markup=UserUpdateValuesKeyboard(field_name=False, set_null=True, not_cancel=True).keyboard)


@dp.message_handler(CheckInputDataFilter(data_type="description"), state=UserRegistrationState.description)
async def set_description(message: Message, state: FSMContext):
    async with state.proxy() as data:
        if data['reg_start'] == True:
            await message.answer("Мы регистрируем ваш профиль, подождите")
            return
        data['reg_start'] = True
        telegram_id = message.from_user.id
        username = message.from_user.username
        name = data['name']
        age = data['age']
        sex = data['sex']
        find_sex = data['find_sex']
        city_data = data['city_id']
        city_from_db = await get_city(name=city_data[1])
        if city_from_db is None:
            await create_city(city_data[1], city_data[0])
            city_from_db = await get_city(name=city_data[1])
        city_id = city_from_db['id']
        description = message.text
        if message.text.lower() == "оставить пустым":
            description = None
        photo_id = data['photo_id']
        video_id = data['video_id']
    await create_user(telegram_id, username, name, age, sex, find_sex, city_id, photo_id, video_id, description)
    await message.answer("Твоя анкета успешно создана", reply_markup=main_menu_keboard)
    await state.finish()
    user_info = {'telegram_id': telegram_id, 'username': username, 'name': name, 'age': age, 'sex': sex, 'find_sex': find_sex, 'city_id': city_id, 'photo_id': photo_id, 'video_id': video_id, 'description': description, 'checked': None, 'check_time': None}
    await user_profile(message, user_info)


@dp.message_handler(CheckInputDataFilter(data_type="description", invalid=True), state=UserRegistrationState.description)
async def invalid_description(message: Message):
    await message.answer("Описание указано не верно, возможные причины:\n❌ Слишком длинное описание (больше 256 символов)\n❌ содержит в себе / или @")
    await message.answer("Попробуйте снова")






@dp.message_handler(UserRoleFilter(role="new_user"))
async def unknown_command(message: Message):
    await start(message)
