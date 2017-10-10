from flask import Blueprint, render_template, request
from flask_login import login_user
from werkzeug.utils import redirect

from gbcma.db.users import UsersRepository
from gbcma.web.app.auth import User

login = Blueprint("login", __name__, template_folder=".")


@login.route("/", methods=['GET', 'POST'])
def index():
    print("WE ARE HERE")
    if request.method == "GET":
        return render_template("login.html")

    elif request.method == "POST":
        rep = UsersRepository()
        data = request.form
        user = rep.find(data["login"], data["password"])
        if user:
            u = User(user)
            login_user(u)
            return redirect("/proposals")
        else:
            return render_template("login.html")


@login.route("/unauthorized")
def unauthorized():
    return render_template("unauthorized.html")
