from flask import Flask

from gbcma.web import proposals

app = Flask(__name__)
app.register_blueprint(proposals, url_prefix="/proposals")
