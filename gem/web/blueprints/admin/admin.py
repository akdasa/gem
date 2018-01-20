from flask import Blueprint, request

from .controller import AdminController

admin = Blueprint("admin", __name__, template_folder=".")
controller = AdminController()


@admin.route("/")
def index():
    return controller.index()


@admin.route("/new", methods=["GET", "POST"])
def create():
    return controller.create(request)


@admin.route("/<string:key>", methods=["GET", "POST", "DELETE"])
def update(key):
    return controller.update(request, key)
