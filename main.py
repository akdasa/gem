import os
from flask import Flask, redirect, request, flash, current_app, send_from_directory, make_response, Response
from flask_login import LoginManager, current_user

from gem.channel import init
from gem.db import users as users_db
from gem.web.app.auth import User, has_permission, access_denied
from gem.web.app.json_encoder import GemJsonEncoder
from gem.web.blueprints.admin import admin
from gem.web.blueprints.proposals import proposals
from gem.web.blueprints.sessions import sessions
from gem.web.blueprints.users import users
from gem.web.blueprints.roles import roles
from gem.web.blueprints.index import index
from gem.web.blueprints.laws import laws
from gem.web.blueprints.search import search


app = Flask(__name__,
            template_folder="gem/web/templates",
            static_folder="gem/web/static")
app.secret_key = 'some_secret'
app.json_encoder = GemJsonEncoder
channel = init(app)

from gem.web.blueprints.account import account
from gem.web.blueprints.session import session

login_manager = LoginManager()

app.register_blueprint(index)
app.register_blueprint(proposals, url_prefix="/proposals")
app.register_blueprint(users, url_prefix="/users")
app.register_blueprint(roles, url_prefix="/roles")
app.register_blueprint(sessions, url_prefix="/sessions")
app.register_blueprint(account, url_prefix="/account")
app.register_blueprint(session, url_prefix="/session")
app.register_blueprint(laws, url_prefix="/laws")
app.register_blueprint(search, url_prefix="/search")
app.register_blueprint(admin, url_prefix="/admin")

login_manager.init_app(app)
login_manager.login_view = "index.index_index"
login_manager.login_message_category = "info"

if __name__ == "__main__":
    channel.run(app)


@app.route('/files/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    uploads = os.path.join(current_app.root_path, "files")
    return send_from_directory(directory=uploads, filename=filename, as_attachment=True)


@app.before_request
def before_request():
    if not current_user:
        return

    if not hasattr(current_user, "suspended"):
        return

    if current_user.suspended and request.path not in ["/account/logout"]:
        return access_denied("Your account has been suspended. Reason: " + current_user.suspend_reason)

    if not current_user.password and request.path not in ["/account/setup", "/account/logout"]:
        return redirect("/account/setup")


@app.add_template_global
def user_has_permission(permission):
    return has_permission(permission)


@login_manager.user_loader
def load_user(user_id):
    user = users_db.get(user_id)
    if user:
        return User(user)
    return None
