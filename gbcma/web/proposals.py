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
        r.create(data["title"], content=data["content"])
        return redirect(url_for("proposals.index"))


@proposals.route("/<string:key>", methods=["GET", "POST"])
def update(key):
    """Shows proposal."""
    r = ProposalsRepository()
    d = r.get(key)

    if request.method == "GET":
        return render_template("view.html", proposal=d)

    elif request.method == "POST":
        data = request.form
        d["title"] = data["title"]
        d["content"] = data["content"]
        r.save(d)
        return redirect(url_for("proposals.index"))