from flask import Blueprint, request, jsonify

from .controller import LawsController

laws = Blueprint("laws", __name__, template_folder=".")
controller = LawsController()


@laws.route("/")
def index():
    return controller.index()


@laws.route("/new", methods=["GET", "POST"])
def create():
    return controller.create(request)


@laws.route("/<string:key>", methods=["GET", "POST", "DELETE"])
def update(key):
    return controller.update(request, key)
