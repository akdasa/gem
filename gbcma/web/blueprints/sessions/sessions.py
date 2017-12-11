from flask import Blueprint, request

from gbcma.web.blueprints.sessions.controller import SessionsController

sessions = Blueprint("sessions", __name__, template_folder=".")
controller = SessionsController()


@sessions.route("/")
def index():
    return controller.index()


@sessions.route("/new", methods=["GET", "POST"])
def create():
    return controller.create(request)


@sessions.route("/<string:key>", methods=["GET", "POST", "DELETE", "PUT"])
def update(key):
    if request.method == "PUT":
        return controller.run(request, key)
    else:
        return controller.update(request, key)
