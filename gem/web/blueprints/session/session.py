from flask import Blueprint, request
from flask_login import login_required, current_user

from gem.channel.channel import get
from gem.web.app.printer.comments import print_comments
from .controller import SessionController

session = Blueprint("session", __name__, template_folder=".")
controller = SessionController()
channel = get()


@session.route("/<string:session_id>")
@login_required
def index(session_id):
    return controller.index(session_id, current_user)


# Messages -------------------------------------------------------------------------------------------------------------

@channel.on("join")
@login_required
def on_join_message(data):
    return controller.join(request.sid, current_user.id, data)


@channel.on("chat")
@login_required
def on_chat_message(data):
    return controller.chat(request.sid, data)


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
    return controller.vote(request.sid, data)


@channel.on("comment")
@login_required
def on_comment_message(data):
    return controller.comment(request.sid, data)


@channel.on("disconnect")
@login_required
def on_disconnect():
    return controller.disconnect(request.sid)


@channel.on("timer")
@login_required
def on_timer(data):
    return controller.set_timer(request.sid, data)


@channel.on("manage")
@login_required
def on_manage(data):
    return controller.manage(request.sid, data)


@channel.on("manage_session")
@login_required
def on_manage_session(data):
    return controller.manage_session(request.sid, data)


@channel.on("kick")
@login_required
def on_kick(data):
    return controller.kick(request.sid, data)


@channel.on("print")
@login_required
def on_print(data):
    path_to_file = print_comments(current_user, {})
    return {"path": path_to_file}
