from aiogram import Dispatcher
from .users import UserRoleFilter, CheckInputDataFilter


def setup_filters(dp: Dispatcher):
    dp.bind_filter(UserRoleFilter)
    dp.bind_filter(CheckInputDataFilter)