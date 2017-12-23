from flask import Blueprint, request

from gem.web.blueprints.users.controller import UsersController

users = Blueprint("users", __name__, template_folder=".")
controller = UsersController()


@users.route("/")
def index():
    return controller.index()


@users.route("/new", methods=["GET", "POST"])
def create():
    return controller.create(request)


@users.route("/<string:key>", methods=["GET", "POST", "DELETE"])
def update(key):
    return controller.update(request, key)
