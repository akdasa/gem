from flask import Blueprint, render_template, request, flash, redirect
from flask_login import login_user, logout_user, current_user, login_required

from gbcma.db.sessions import SessionsRepository
from gbcma.db.users import UsersRepository
from gbcma.web.app.auth import User

account = Blueprint("account", __name__, template_folder=".")
rep = UsersRepository()
sessions = SessionsRepository()


@account.route("/", methods=["GET", "POST"])
@login_required
def index():
    return render_template("account_dashboard.html",
                           active=list(sessions.active()),
                           upcoming=list(sessions.upcoming()))


@account.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "GET":
        return render_template("account_edit.html")

    elif request.method == "POST":
        data = request.form
        name = data.get("name", "<Noname das>")
        d = rep.get(current_user.get_id())
        d["name"] = name
        rep.save(d)
        return redirect("/account")


@account.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template("login.html")

    elif request.method == "POST":
        data = request.form
        login = data.get("login", None)
        password = data.get("password", None)
        user = rep.find({"login": login, "password": password})

        if user:
            u = User(user)
            login_user(u)
            flash("You have successfully logged in", category="success")
            return redirect("/account")
        else:
            flash("User with specified login/password pair not found", category="danger")
            return render_template("login.html")


@account.route("/logout")
def logout():
    logout_user()
    flash("You have successfully logged out", category="success")
    return render_template("login.html")
