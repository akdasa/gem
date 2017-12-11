from flask import Blueprint, request, jsonify

from .controller import ProposalsController

proposals = Blueprint("proposals", __name__, template_folder=".")
controller = ProposalsController()


@proposals.route("/")
def index():
    return controller.index()


@proposals.route("/new", methods=["GET", "POST"])
def create():
    return controller.create(request)


@proposals.route("/<string:key>", methods=["GET", "POST", "DELETE"])
def update(key):
    return controller.update(request, key)


@proposals.route("/search")
def search():
    return jsonify(controller.search(request))
