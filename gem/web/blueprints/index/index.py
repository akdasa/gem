from flask_login import current_user

from gem.db import sessions
from flask import Blueprint, render_template

index = Blueprint("index", __name__, template_folder=".")


@index.route("/", methods=["GET", "POST"])
def index_index():
    return render_template("index_index.html",
                           upcoming_sessions=__upcoming_sessions_for_user(current_user),
                           active_sessions=__active_sessions_for_user(current_user))


def __upcoming_sessions_for_user(user):
    if user and hasattr(user, "role"):
        upcoming = sessions.upcoming()
        result = filter(lambda x: x.get("status", None) != "run", upcoming)
        return list(result)[:5]
    return []

def __active_sessions_for_user(user):
    if user and hasattr(user, "role"):
        upcoming = sessions.active()
        return list(upcoming)[:3]
    return []