from flask import Blueprint, render_template
from flask_login import login_required

sessions = Blueprint("sessions", __name__, template_folder=".")


@sessions.route("/")
@login_required
def index():
    return render_template("sessions_index.html")
