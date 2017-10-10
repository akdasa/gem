from flask import Flask
from flask_login import LoginManager, current_user

from gbcma.db.users import UsersRepository
from gbcma.web import login
from gbcma.web import proposals
from gbcma.web.app.auth import User

app = Flask(__name__,
            template_folder="gbcma/web/templates",
            static_folder="gbcma/web/static")
app.secret_key = 'some_secret'
login_manager = LoginManager()
app.register_blueprint(proposals, url_prefix="/proposals")
app.register_blueprint(login, url_prefix="/login")

login_manager.init_app(app)
login_manager.login_view = "login.index"
login_manager.login_message_category = "info"


@app.add_template_global
def user_has_role(role):
    if not current_user:
        return False
    return current_user.has_role(role)

@login_manager.user_loader
def load_user(user_id):
    r = UsersRepository()
    return User(r.get(user_id))

