from flask import Blueprint, render_template, request, flash
from flask_login import login_user, logout_user
from werkzeug.utils import redirect

from gbcma.db.users import UsersRepository
from gbcma.web.app.auth import User

account = Blueprint("account", __name__, template_folder=".")


@account.route("/")
def index():
    return render_template("account.html")


@account.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template("login.html")

    elif request.method == "POST":
        rep = UsersRepository()
        data = request.form
        user = rep.find(data["login"], data["password"])
        if user:
            u = User(user)
            login_user(u)
            flash("You have successfully logged in", category="success")
            return redirect("/proposals")
        else:
            flash("User with specified login/password pair not found", category="danger")
            return render_template("login.html")


@account.route("/logout")
def logout():
    logout_user()
    flash("You have successfully logged out", category="success")
    return render_template("login.html")
