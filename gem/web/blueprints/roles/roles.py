from flask import Blueprint, request

from .controller import RolesController

roles = Blueprint("roles", __name__, template_folder=".")
controller = RolesController()


@roles.route("/")
def index():
    return controller.index()


@roles.route("/new", methods=["GET", "POST"])
def create():
    return controller.create(request)


@roles.route("/<string:key>", methods=["GET", "POST", "DELETE"])
def update(key):
    return controller.update(request, key)
