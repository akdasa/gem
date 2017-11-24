from flask import Blueprint, render_template

index = Blueprint("index", __name__, template_folder=".")


@index.route("/", methods=["GET", "POST"])
def index_index():
    return render_template("index_index.html")
