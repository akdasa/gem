from flask import Blueprint, request
from flask_login import login_required

from gbcma.db.roles import RolesRepository
from .controller import RolesController

roles = Blueprint("roles", __name__, template_folder=".")
controller = RolesController(
    repository=RolesRepository()
)


@roles.route("/")
@login_required
def index():
    return controller.index()


@roles.route("/new", methods=["GET", "POST"])
@login_required
def create():
    return controller.create(request)


@roles.route("/<string:key>", methods=["GET", "POST", "DELETE"])
@login_required
def update(key):
    return controller.update(request, key)
