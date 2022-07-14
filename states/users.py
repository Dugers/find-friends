from aiogram.dispatcher.filters.state import StatesGroup, State

class UserRegistrationState(StatesGroup):
    name = State()
    age = State()
    sex = State()
    find_sex = State()
    city_id = State()
    photo_id = State()
    description = State()


class UserUpdateState(StatesGroup):
    name = State()
    age = State()
    sex = State()
    find_sex = State()
    city_id = State()
    photo_id = State()
    description = State()

class FindState(StatesGroup):
    inSearch = State()
    reaction = State()
    text = State()

class LikeState(StatesGroup):
    reaction = State()