from flask import Flask
from flask_login import LoginManager

from gbcma.db.users import UsersRepository
from gbcma.web.blueprints.account import account
from gbcma.web.blueprints.proposals import proposals
from gbcma.web.blueprints.users import users
from gbcma.web.app.auth import User, has_permission

app = Flask(__name__,
            template_folder="gbcma/web/templates",
            static_folder="gbcma/web/static")
app.secret_key = 'some_secret'
login_manager = LoginManager()
app.register_blueprint(proposals, url_prefix="/proposals")
app.register_blueprint(users, url_prefix="/users")
app.register_blueprint(account, url_prefix="/account")

login_manager.init_app(app)
login_manager.login_view = "account.login"
login_manager.login_message_category = "info"


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
