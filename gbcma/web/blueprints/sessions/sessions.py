from flask import Blueprint, request
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


@sessions.route("/<string:key>", methods=["GET", "POST", "DELETE"])
@login_required
def update(key):
    return controller.update(request, key)
