from functools import wraps

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
