from flask import Blueprint
from flask_login import login_user

from gbcma.channel.channel import get
from gbcma.db import users
from gbcma.web.app.auth import User
from .controllers import DashboardController, LoginController, AccountController

account = Blueprint("account", __name__, template_folder=".")
channel = get()


@account.route("/")
def index():
    return DashboardController().index()


@account.route("/setup", methods=["GET", "POST"])
def setup():
    return AccountController().edit(setup=True)


@account.route("/edit", methods=["GET", "POST"])
def edit():
    return AccountController().edit()


@account.route("/login", methods=['GET', 'POST'])
def login():
    return LoginController().login()


@account.route("/logout")
def logout():
    return LoginController().logout()


# Messages

@channel.on("login")
def on_login_message(data):
    user = users.find_one(
        {"$and": [{"password": data["password"]}, {"$or": [{"login": data["login"]}, {"name": data["login"]}]}]})

    if user:
        u = User(user)
        login_user(u)
