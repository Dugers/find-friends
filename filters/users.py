from data import ADMIN_ID
from aiogram.types import Message
from aiogram.dispatcher.handler import ctx_data
from aiogram.dispatcher.filters import BoundFilter

class UserRoleFilter(BoundFilter):
    # role types:
    # new_user - unregisted user
    # user - registed user
    # admin - registed user and admin.id == ADMIN_ID

    def __init__(self, role):
        self.role = role

    async def check(self, message: Message):
        user_info = ctx_data.get()['user_info']
        if user_info is None:
            if self.role == "new_user":
                return True
            return False
        if self.role == "new_user":
            return False
        if user_info['telegram_id'] == ADMIN_ID:
            return True
        if self.role == "user":
            return True
        return False


class CheckInputDataFilter(BoundFilter):
    # data types:
    # name - string lenght - [3:30] 
    # age - integer - [10:100]
    # description - string lenght - [1:256]

    def __init__(self, data_type, invalid=False):
        self.data_type = data_type
        self.i = 0
        if invalid:
            self.i = 1

    async def check(self, message: Message):
        data = message.text
        if self.data_type in ['name', 'description']:
            if data[0] == "/" or "@" in data:
                return [False, True][self.i]
        if self.data_type == "name":
            if data.isdigit():
                return [False, True][self.i]
            elif not (len(data) >= 3 and len(data) <= 30):
                return [False, True][self.i]
            else:
                return [True, False][self.i]
        elif self.data_type == "age":
            if not data.isdigit():
                return [False, True][self.i]
            elif not (int(data) >= 10 and int(data) <= 100):
                return [False, True][self.i]
            else:
                return [True, False][self.i]
        elif self.data_type == "description":
            if not (len(data) <= 256):
                return [False, True][self.i]
            return [True, False][self.i]