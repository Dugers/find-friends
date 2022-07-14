from loader import dp
from filters import UserRoleFilter, CheckInputDataFilter 
from states import UserUpdateState
from utils.db import get_city, create_city, update_user
from utils.geo import get_geowork
from keyboards.default import UserUpdateValuesKeyboard, main_menu_keboard
from keyboards.inline import profile_settings_keyboard, update_sex_keyboard, update_find_sex_keyboard
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

@dp.message_handler(UserRoleFilter(role="user"), lambda message: message.text.lower() == "мой профиль")
async def user_profile(message: Message, user_info):
    user_city = await get_city(id=user_info['city_id'])
    text = f"{user_info['name']}, {user_info['age']}, {user_city['name']}\nПол: "
    if user_info['sex'] == "M":
        text += "Мужской"
    else:
        text += "Женский"
    text += "\nВ поисках: "
    if user_info['find_sex'].strip() == "M":
        text += "Парней"
    elif user_info['find_sex'].strip() == "F":
        text += "Девушек"
    else:
        text += "Всех"
    if user_info['description']:
        text += f"\nОписание: {user_info['description']}"
    if user_info['photo_id']:
        await message.answer_photo(user_info['photo_id'])
    else:
        await message.answer_video(user_info['video_id'])
    await message.answer(text, reply_markup=profile_settings_keyboard)


@dp.message_handler(lambda message: message.text.lower() == "отмена", state=UserUpdateState)
async def cancel_update_user(message: Message, state: FSMContext):
    await state.finish()
    await message.answer("Изменения отменены", reply_markup=main_menu_keboard)


@dp.callback_query_handler(text="cancel", state=UserUpdateState)
async def cancel_query_update_user(callback: CallbackQuery, state: FSMContext, user_info):
    await callback.message.delete()
    await state.finish()
    await callback.message.answer("Изменения отменены", reply_markup=main_menu_keboard)


@dp.callback_query_handler(text="update_name")
async def user_set_name(callback: CallbackQuery, user_info):
    await callback.answer()
    keyboard = UserUpdateValuesKeyboard(value=user_info['name']).keyboard
    await UserUpdateState.name.set()
    await callback.message.answer("Введите новое имя", reply_markup=keyboard)


@dp.message_handler(CheckInputDataFilter(data_type="name"), state=UserUpdateState.name)
async def user_update_name(message: Message, state: FSMContext):
    await update_user(message.from_user.id, name=message.text)
    await state.finish()
    await message.answer("Имя успешно изменено", reply_markup=main_menu_keboard)


@dp.message_handler(CheckInputDataFilter(data_type="name", invalid=True), state=UserUpdateState.name)
async def user_invalid_name(message: Message):
    await message.answer("Имя указано не правильно, возможные причины:\n❌ Слишком короткое (меньше 3 символов) или слишком длинное (больше 30 символов)\n❌ Является числом\n❌ Начинается с / или содержит @")
    await message.answer("Попробуйте снова")


@dp.callback_query_handler(text="update_age")
async def user_set_age(callback: CallbackQuery, user_info):
    await callback.answer()
    keyboard = UserUpdateValuesKeyboard(user_info['age']).keyboard 
    await UserUpdateState.age.set()
    await callback.message.answer("Введите новый возраст", reply_markup=keyboard)


@dp.message_handler(CheckInputDataFilter(data_type="age"), state=UserUpdateState.age)
async def user_update_name(message: Message, state: FSMContext):
    await update_user(message.from_user.id, age=int(message.text))
    await state.finish()
    await message.answer("Возраст успешно изменен", reply_markup=main_menu_keboard)


@dp.message_handler(CheckInputDataFilter(data_type="age", invalid=True), state=UserUpdateState.age)
async def user_invalid_name(message: Message):
    await message.answer("Возраст указан не правильно, возможные причины:\n❌ Не является числом\n❌ Больше 100 или меньше 10")
    await message.answer("Попробуйте снова")


@dp.callback_query_handler(text="update_sex")
async def user_set_sex(callback: CallbackQuery):
    await callback.answer()
    keyboard = update_sex_keyboard
    await UserUpdateState.sex.set()
    await callback.message.answer("Выберите свой пол", reply_markup=keyboard)


@dp.callback_query_handler(lambda callback: callback.data in ['sex_M', 'sex_F'], state=UserUpdateState.sex)
async def user_update_sex(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.finish()
    await update_user(callback.from_user.id, sex=callback.data.replace('sex_', ''))
    await callback.message.answer("Пол изменен успешно")


@dp.callback_query_handler(text="update_find_sex")
async def user_set_find_sex(callback: CallbackQuery):
    await callback.answer()
    keyboard = update_find_sex_keyboard
    await UserUpdateState.find_sex.set()
    await callback.message.answer("Выберите кто вас интересуют", reply_markup=keyboard)


@dp.callback_query_handler(lambda callback: callback.data in ['find_sex_M', 'find_sex_F', 'find_sex_MF'], state=UserUpdateState.find_sex)
async def user_update_find_sex(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await update_user(callback.from_user.id, find_sex=callback.data.replace('find_sex_', ''))
    await callback.message.answer("Предпочтения обновлены успешно")
    await state.finish()

@dp.callback_query_handler(text="update_photo_video")
async def user_set_photo_video(callback: CallbackQuery):
    await callback.answer()
    keyboard = UserUpdateValuesKeyboard(field_name=False).keyboard
    await UserUpdateState.photo_id.set()
    await callback.message.answer("Отправьте одну фотографию или одно видео", reply_markup=keyboard)


@dp.message_handler(content_types=['photo', 'video'], state=UserUpdateState.photo_id)
async def user_update_photo_video(message: Message, state: FSMContext):
    try:
        photo_id = message.photo[0].file_id
        video_id = None
    except:
        video_id = message.video.file_id
        photo_id = None
    await state.finish()
    await update_user(message.from_user.id, photo_id=photo_id, video_id=video_id)
    await message.answer("Фото/видео успешно обновлено", reply_markup=main_menu_keboard)

@dp.callback_query_handler(text="update_description")
async def user_set_description(callback: CallbackQuery):
    await callback.answer()
    keyboard = UserUpdateValuesKeyboard(field_name=False, set_null=True).keyboard
    await UserUpdateState.description.set()
    await callback.message.answer("Введите новое описание", reply_markup=keyboard)


@dp.message_handler(CheckInputDataFilter(data_type="description"), state=UserUpdateState.description)
async def user_update_description(message: Message, state: FSMContext):
    await state.finish()
    description = message.text
    if description.lower() == "оставить пустым":
        description = None
    await update_user(message.from_user.id, description=description)
    await message.answer("Описание обновлено", reply_markup=main_menu_keboard)


@dp.message_handler(CheckInputDataFilter(data_type="description", invalid=True), state=UserUpdateState.description)
async def user_invalid_description(message: Message):
    await message.answer("Описание указано не верно, возможные причины:\n❌ Слишком длинное описание (больше 256 символов)\n❌ содержит в себе / или @")
    await message.answer("Попробуйте снова")


@dp.callback_query_handler(text="update_city")
async def user_set_city(callback: CallbackQuery, state:FSMContext, user_info):
    await callback.answer()
    user_city = await get_city(id=user_info['city_id'])
    keyboard = UserUpdateValuesKeyboard(value=user_city['name'], field_name='city').keyboard
    await UserUpdateState.city_id.set()
    async with state.proxy() as data:
        data['city_id'] = False
    await callback.message.answer("Введите название города или отправьте метку", reply_markup=keyboard)


@dp.message_handler(CheckInputDataFilter(data_type="name"), state=UserUpdateState.city_id)
async def user_update_city_text(message: Message, state: FSMContext):
    async with state.proxy() as data:
        if data['city_id'] == False:
            data['city_id'] = True
        else:
            await message.answer("Проверяем ваш город, подождите")
            return
    await message.answer("Ожидайте (до 30 секунд)")
    city_data = await get_geowork(name=message.text, need_name=True, need_coordinates=True)
    if city_data:
        city_from_db = await get_city(name=city_data[1])
        if city_from_db is None:
            await create_city(city_data[1], city_data[0])
            city_from_db = await get_city(name=city_data[1])
        city_id = city_from_db['id']
        await update_user(message.from_user.id, city_id=city_id)
        await state.finish()
        await message.answer("Ура! Мы смогли найти ваш город на карте\nГород успешно изменен", reply_markup=main_menu_keboard)
    else:
        await message.answer("Город указан не верно, попробуйте снова")
        async with state.proxy() as data:
            data['city_id'] = False


@dp.message_handler(CheckInputDataFilter(data_type="name", invalid=True), state=UserUpdateState.city_id)
async def user_invalid_city_text(message: Message):
    await message.answer("Название города указано не правильно, возможные причины:\n❌ Название слишком длинное или короткое\n❌ Содержит / или @")
    await message.answer("Попробуйте снова")


@dp.message_handler(content_types=['location'], state=UserUpdateState.city_id)
async def set_city_id_location(message: Message, state: FSMContext):
    coordinates = (message.location.latitude, message.location.longitude)
    city_data = await get_geowork(coordinates=coordinates, need_name=True, need_coordinates=True)
    if city_data:
        city_from_db = await get_city(name=city_data[1])
        if city_from_db is None:
            await create_city(city_data[1], city_data[0])
            city_from_db = await get_city(name=city_data[1])
        city_id = city_from_db['id']
        await update_user(message.from_user.id, city_id=city_id)
        await state.finish()
        await message.answer("Ура! Мы смогли найти ваш город на карте\nГород успешно изменен", reply_markup=main_menu_keboard)
    else:
        await state.finish()
        await message.answer("Технические неполадки, попробуйте позже")