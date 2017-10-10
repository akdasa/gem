from flask import Blueprint, render_template, request, url_for, jsonify, flash
from flask_login import login_required
from werkzeug.utils import redirect

from gbcma.db.proposals import ProposalsRepository
from gbcma.web.app.auth import requires_permissions

proposals = Blueprint("proposals", __name__, template_folder=".")


@proposals.route("/")
@login_required
@requires_permissions(["proposal.list"])
def index():
    """Shows list of proposals to process."""
    r = ProposalsRepository()
    return render_template("index.html", proposals=r.find())


@proposals.route("/new", methods=["GET", "POST"])
@login_required
@requires_permissions(["proposal.create"])
def new():
    """Creates new proposal."""
    r = ProposalsRepository()

    if request.method == "GET":
        return render_template("new.html", proposal=None)

    elif request.method == "POST":
        data = request.form
        r.create(data["title"], content=data["content"])
        flash("Proposal was successfully created", category="success")
        return redirect(url_for("proposals.index"))


@proposals.route("/<string:key>", methods=["GET", "POST", "DELETE"])
@login_required
@requires_permissions(["proposal.update"])
def update(key):
    """Shows proposal."""
    r = ProposalsRepository()

    if request.method == "GET":
        d = r.get(key)
        return render_template("view.html", proposal=d)

    elif request.method == "POST":
        d = r.get(key)
        data = request.form
        d["title"] = data["title"]
        d["content"] = data["content"]
        r.save(d)
        flash("Proposal was successfully updated", category="success")
        return redirect(url_for("proposals.index"))

    elif request.method == "DELETE":
        r.delete(key)
        return jsonify({"success": True})
