from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu_keboard = ReplyKeyboardMarkup(resize_keyboard=True)
my_profile_button = KeyboardButton("Мой профиль")
find_button = KeyboardButton("Искать")
main_menu_keboard.add(my_profile_button, find_button)

cancel_search_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton("Закончить поиск"))

return_to_find_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton("Вернуться обратно"))


class UserUpdateValuesKeyboard:
    def __init__(self, value=None, field_name=True, set_null=False, not_cancel=False):
        self.value = value
        self.field_name = field_name
        self.set_null = set_null
        self.not_cancel = not_cancel
    
    @property
    def keyboard(self):
        if (self.field_name):
            if self.field_name == 'city':
                keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1).add(KeyboardButton(text="Отправить геолокацию", request_location=True))
                if self.value:
                    keyboard.add(KeyboardButton(text=self.value))
                    keyboard.add(KeyboardButton(text="Отмена"))
                return keyboard
            keyboard =  ReplyKeyboardMarkup(resize_keyboard=True, row_width=1).add(KeyboardButton(text=self.value), KeyboardButton(text="Отмена"))
            if self.set_null:
                keyboard.add(KeyboardButton(text="Оставить пустым"))
            return keyboard
        else:
            keyboard =  ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            if self.set_null:
                keyboard.add(KeyboardButton(text="Оставить пустым"))
            if self.not_cancel:
                return keyboard
            keyboard.add(KeyboardButton(text="Отмена"))
            return keyboard