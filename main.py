from flask import Flask

from gbcma.web import proposals

app = Flask(__name__,
            template_folder="gbcma/web/templates",
            static_folder="gbcma/web/static")
app.secret_key = 'some_secret'
app.register_blueprint(proposals, url_prefix="/proposals")
