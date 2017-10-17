from flask import Blueprint, request, jsonify
from flask_login import login_required

from gbcma.db.sessions import SessionsRepository
from gbcma.web.blueprints.sessions.controller import SessionsController

sessions = Blueprint("sessions", __name__, template_folder=".")
controller = SessionsController(
    repository=SessionsRepository()
)


@sessions.route("/")
@login_required
def index():
    return controller.index()


@sessions.route("/new", methods=["GET", "POST"])
@login_required
def create():
    return controller.create(request)


@sessions.route("/<string:key>", methods=["GET", "POST", "DELETE", "PUT"])
@login_required
def update(key):
    if request.method == "PUT":
        return controller.run(request, key)
    else:
        return controller.update(request, key)
