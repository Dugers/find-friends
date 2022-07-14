from multiprocessing.managers import DictProxy
from .users import UserRoleMiddleware


def setup_middlewares(dp):
    dp.setup_middleware(UserRoleMiddleware())