from flask import Blueprint

from .controllers import DashboardController, LoginController, AccountController

account = Blueprint("account", __name__, template_folder=".")


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
