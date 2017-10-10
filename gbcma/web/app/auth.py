from functools import wraps

from flask_login import UserMixin
from flask_login import current_user
from werkzeug.utils import redirect


def get_current_user_role():
    if current_user:
        return current_user.roles
    return None


def requires_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if not set(get_current_user_role()) >= set(roles[0]):
                return redirect("/login/unauthorized")
            return f(*args, **kwargs)
        return wrapped
    return wrapper


class User(UserMixin):
    def __init__(self, dict):
        print("DDD", dict)
        self.__id = str(dict["_id"])
        self.__name = dict.get("name", "<Noname das>")
        self.__roles = dict.get("roles", [])

    def get_id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def roles(self):
        return self.__roles

    def has_role(self, name):
        return name in self.__roles
