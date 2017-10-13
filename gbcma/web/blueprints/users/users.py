from flask import Blueprint, request
from flask_login import login_required

from gbcma.db.users import UsersRepository
from gbcma.web.blueprints.users.controller import UsersController

users = Blueprint("users", __name__, template_folder=".")
controller = UsersController(
    repository=UsersRepository()
)


@users.route("/")
@login_required
def index():
    return controller.index()


@users.route("/new", methods=["GET", "POST"])
@login_required
def create():
    return controller.create(request)


@users.route("/<string:key>", methods=["GET", "POST", "DELETE"])
@login_required
def update(key):
    return controller.update(request, key)
