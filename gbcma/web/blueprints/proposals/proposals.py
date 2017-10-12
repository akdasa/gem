from flask import Blueprint, render_template, request, jsonify, flash, redirect
from flask_login import login_required

from gbcma.db.proposals import ProposalsRepository
from gbcma.web.app.auth import has_permission, have_no_permissions

proposals = Blueprint("proposals", __name__, template_folder=".")
rep = ProposalsRepository()


@proposals.route("/")
@login_required
def index():
    """Shows list of proposals to process."""
    if has_permission("proposals.read"):
        plist = rep.all()  # get all proposals to show
        return render_template("proposals_index.html",
                               proposals=plist,
                               show_actions=has_permission("proposals.delete"),
                               show_delete=has_permission("proposals.delete"))
    else:
        return have_no_permissions()


@proposals.route("/new", methods=["GET", "POST"])
@login_required
def create():
    """Creates new proposal."""
    if not has_permission("proposals.create"):
        return have_no_permissions()

    if request.method == "GET":
        return render_template("proposals_new.html", proposal=None)

    elif request.method == "POST":
        doc = __form_to_dict(request.form, {})
        rep.insert(doc)
        flash("Proposal was successfully created", category="success")
        return redirect("/proposals")


@proposals.route("/<string:key>", methods=["GET", "POST", "DELETE"])
@login_required
def update(key):
    """Shows proposal."""
    if request.method == "GET":
        if has_permission("proposals.read"):
            return render_template("proposals_view.html", proposal=rep.get(key))
        else:
            return have_no_permissions()

    elif request.method == "POST":
        if has_permission("proposals.update"):
            proposal = rep.get(key)
            doc = __form_to_dict(request.form, proposal)
            rep.save(doc)
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


def __form_to_dict(form, d):
    d.update({
        "title": form.get("title", "<No title>"),
        "content": form.get("content", "<No content>")
    })
    return d
