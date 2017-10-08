from flask import Blueprint, render_template

from gbcma.db.proposals import ProposalsRepository

proposals = Blueprint("proposals", __name__, template_folder=".")


@proposals.route("/")
def index():
    r = ProposalsRepository()
    return render_template("index.html", proposals=r.find())
