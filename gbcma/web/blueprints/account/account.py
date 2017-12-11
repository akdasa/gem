import itertools

from flask import Blueprint, render_template, request, flash, redirect
from flask_login import login_user, logout_user, current_user, login_required

from gbcma.db.proposals import ProposalsRepository
from gbcma.db.sessions import SessionsRepository
from gbcma.db.users import UsersRepository
from gbcma.web.app.auth import User

account = Blueprint("account", __name__, template_folder=".")
rep = UsersRepository()
sessions = SessionsRepository()
prop = ProposalsRepository()


@account.route("/", methods=["GET", "POST"])
@login_required
def index():
    user = current_user

    # loads all proposals objects of sessions
    sessions_list = list(filter(lambda x: user.role in x["permissions"]["presence"], sessions.upcoming()))
    proposal_ids = map(lambda x: x.get("proposals"), sessions_list)
    proposal_ids = list(itertools.chain(*proposal_ids))
    proposal_objects = prop.find({"_id": {"$in": proposal_ids}})
    proposal_objects = {key["_id"]: key for key in proposal_objects}

    return render_template("account_dashboard.html",
                           sessions=sessions_list,
                           proposals=proposal_objects)


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
        lgn = data.get("login", None)
        password = data.get("password", None)
        user = rep.find_one({"login": lgn, "password": password})

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
