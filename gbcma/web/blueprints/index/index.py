from flask_login import current_user

from gbcma.db import sessions
from flask import Blueprint, render_template

index = Blueprint("index", __name__, template_folder=".")


@index.route("/", methods=["GET", "POST"])
def index_index():
    return render_template("index_index.html",
                           sessions=__upcoming_sessions_for_user(current_user))


def __upcoming_sessions_for_user(user):
    if user and hasattr(user, "role"):
        upcoming = sessions.upcoming()
        result = filter(lambda x: user.role in x["permissions"]["presence"], upcoming)
        return list(result)
    return []
