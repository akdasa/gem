from flask import Blueprint, request
from flask_login import login_required

from gbcma.db.proposals import ProposalsRepository
from gbcma.web.blueprints.proposals.controller import ProposalsController

proposals = Blueprint("proposals", __name__, template_folder=".")
controller = ProposalsController(
    repository=ProposalsRepository()
)


@proposals.route("/")
@login_required
def index():
    return controller.index()


@proposals.route("/new", methods=["GET", "POST"])
@login_required
def create():
    return controller.create(request)


@proposals.route("/<string:key>", methods=["GET", "POST", "DELETE"])
@login_required
def update(key):
    return controller.update(request, key)


@proposals.route("/search")
@login_required
def search():
    return controller.search(request)
