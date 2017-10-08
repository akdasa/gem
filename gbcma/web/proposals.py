from flask import Blueprint, render_template, request, url_for
from werkzeug.utils import redirect

from gbcma.db.proposals import ProposalsRepository

proposals = Blueprint("proposals", __name__, template_folder=".")


@proposals.route("/")
def index():
    """Shows list of proposals to process."""
    r = ProposalsRepository()
    return render_template("index.html", proposals=r.find())


@proposals.route("/new", methods=["GET", "POST"])
def new():
    """Creates new proposal."""
    r = ProposalsRepository()

    if request.method == "GET":
        return render_template("new.html")

    elif request.method == "POST":
        data = request.form
        r.create(data["title"])
        return redirect(url_for("proposals.index"))
