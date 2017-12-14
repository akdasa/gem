from flask import Flask, redirect, request, flash
from flask_login import LoginManager, current_user

from gbcma.channel import init
from gbcma.db.users import UsersRepository
from gbcma.web.app.auth import User, has_permission, access_denied
from gbcma.web.blueprints.account import account
from gbcma.web.blueprints.proposals import proposals
from gbcma.web.blueprints.sessions import sessions
from gbcma.web.blueprints.users import users
from gbcma.web.blueprints.roles import roles
from gbcma.web.blueprints.index import index


app = Flask(__name__,
            template_folder="gbcma/web/templates",
            static_folder="gbcma/web/static")
app.secret_key = 'some_secret'
channel = init(app)

from gbcma.web.blueprints.session import session

login_manager = LoginManager()

app.register_blueprint(index)
app.register_blueprint(proposals, url_prefix="/proposals")
app.register_blueprint(users, url_prefix="/users")
app.register_blueprint(roles, url_prefix="/roles")
app.register_blueprint(sessions, url_prefix="/sessions")
app.register_blueprint(account, url_prefix="/account")
app.register_blueprint(session, url_prefix="/session")

login_manager.init_app(app)
login_manager.login_view = "account.login"
login_manager.login_message_category = "info"

if __name__ == "__main__":
    channel.run(app)


@app.before_request
def before_request():
    if not current_user:
        return

    if not hasattr(current_user, "suspended"):
        return

    if current_user.suspended:
        return access_denied("Your account has been suspended. Reason: " + current_user.suspend_reason)

    if not current_user.password and request.path not in ["/account/setup", "/account/logout"]:
        return redirect("/account/setup")


@app.add_template_global
def user_has_permission(permission):
    return has_permission(permission)


@login_manager.user_loader
def load_user(user_id):
    r = UsersRepository()
    user = r.get(user_id)
    if user:
        return User(user)
    return None
