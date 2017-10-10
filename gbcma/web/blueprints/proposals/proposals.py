from flask import Blueprint, render_template, request, jsonify, flash
from flask_login import login_required
from werkzeug.utils import redirect

from gbcma.db.proposals import ProposalsRepository
from gbcma.web.app.auth import has_permission, have_no_permissions

proposals = Blueprint("proposals", __name__, template_folder=".")
rep = ProposalsRepository()


@proposals.route("/")
@login_required
def index():
    """Shows list of proposals to process."""
    if has_permission("proposals.read"):
        pl = rep.find()  # get all proposals to show
        return render_template("index.html", proposals=pl)
    else:
        return have_no_permissions()


@proposals.route("/new", methods=["GET", "POST"])
@login_required
def create():
    """Creates new proposal."""
    if not has_permission("proposals.create"):
        return have_no_permissions()

    if request.method == "GET":
        return render_template("new.html", proposal=None)

    elif request.method == "POST":
        data = request.form
        title = data.get("title", None) or "<No title>"
        content = data.get("content", None) or "<No content>"
        rep.create(title, content=content)
        flash("Proposal was successfully created", category="success")
        return redirect("/proposals")


@proposals.route("/<string:key>", methods=["GET", "POST", "DELETE"])
@login_required
def update(key):
    """Shows proposal."""
    if request.method == "GET":
        if has_permission("proposals.read"):
            return render_template("view.html", proposal=rep.get(key))
        else:
            return have_no_permissions()

    elif request.method == "POST":
        if has_permission("proposals.update"):
            d = rep.get(key)
            data = request.form
            d["title"] = data["title"]
            d["content"] = data["content"]
            rep.save(d)
            flash("Proposal was successfully updated", category="success")
            return redirect("/proposals")
        else:
            return have_no_permissions()

    if request.method == "DELETE":
        if has_permission("proposals.delete"):
            rep.delete(key)
            return jsonify({"success": True})
        else:
            return jsonify({"success": False})
