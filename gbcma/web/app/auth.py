from functools import wraps

from flask import render_template
from flask_login import UserMixin, login_required
from flask_login import current_user
from werkzeug.utils import redirect


def access_denied(message=None):
    return render_template("permission_denied.html", message=message)


def has_permission(permission):
    if permission in get_current_user_permissions():
        return True


def get_current_user_permissions():
    if current_user and hasattr(current_user, "permissions"):
        return current_user.permissions
    return []


def permissions_required(*permissions):
    def wrapper(f):
        @login_required
        @wraps(f)
        def wrapped(*args, **kwargs):
            if not set(get_current_user_permissions()) >= set(permissions[0]):
                return redirect("/login/unauthorized")
            return f(*args, **kwargs)
        return wrapped
    return wrapper


class User(UserMixin):
    def __init__(self, dict):
        self.__id = str(dict["_id"])
        self.__name = dict.get("name", "<Noname das>")
        self.__permissions = dict.get("permissions", [])

    def get_id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def permissions(self):
        return self.__permissions

    def has_permission(self, name):
        return name in self.__permissions
