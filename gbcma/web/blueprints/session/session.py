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


# Messages -------------------------------------------------------------------------------------------------------------

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


@channel.on("raise_hand")
@login_required
def on_raise_hand_message(data):
    return controller.raise_hand(request.sid, current_user, data)


@channel.on("withdraw_hand")
@login_required
def on_raise_hand_message(data):
    return controller.withdraw_hand(request.sid, current_user, data)


@channel.on("give_voice")
@login_required
def on_give_voice_message(data):
    return controller.give_voice(request.sid, current_user, data)


@channel.on("disconnect")
@login_required
def on_disconnect():
    return controller.disconnect(request.sid)


@channel.on("timer")
@login_required
def on_timer(data):
    return controller.set_timer(request.sid, data)