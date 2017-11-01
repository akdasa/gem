from flask import Blueprint, request
from flask_login import login_required, current_user

from gbcma.channel.channel import get
from .controller import SessionController

session = Blueprint("session", __name__, template_folder=".")
controller = SessionController()
channel = get()


@session.route("/<string:session_id>")
@login_required
def index(session_id):
    return controller.index(session_id, current_user, manage=False)


@session.route("/<string:session_id>/manage")
@login_required
def manage(session_id):
    return controller.index(session_id, current_user, manage=True)


@channel.on("join")
def on_join_message(data):
    return controller.join(request.sid, current_user, data)


@channel.on("chat")
def on_chat_message(data):
    return controller.chat(request.sid, current_user, data)


@channel.on("next")
def on_next_message(data):
    return controller.move(request.sid, data)


@channel.on("close")
def on_close_message():
    return controller.close(request.sid)


@channel.on("vote")
def on_vote_message(data):
    return controller.vote(request.sid, current_user, data)


@channel.on("disconnect")
def on_disconnect():
    return controller.disconnect(request.sid)
