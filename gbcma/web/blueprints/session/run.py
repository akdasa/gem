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
@login_required
def on_join_message(data):
    return controller.join(request.sid, current_user, data)


@channel.on("chat")
@login_required
def on_chat_message(data):
    return controller.chat(request.sid, current_user, data)


@channel.on("change_stage")
@login_required
def on_change_stage_message(data):
    return controller.change_stage(request.sid, data)


@channel.on("close")
@login_required
def on_close_message():
    return controller.close(request.sid)


@channel.on("vote")
@login_required
def on_vote_message(data):
    return controller.vote(request.sid, current_user, data)


@channel.on("comment")
@login_required
def on_comment_message(data):
    return controller.comment(request.sid, current_user, data)


@channel.on("disconnect")
@login_required
def on_disconnect():
    return controller.disconnect(request.sid)
