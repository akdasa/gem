from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from flask_socketio import emit

from gbcma.channel.channel import get
from gbcma.db.proposals import ProposalsRepository
from gbcma.db.sessions import SessionsRepository
from gbcma.web.blueprints.run.controller import Controller

run = Blueprint("run", __name__, template_folder=".")
channel = get()
srep = SessionsRepository()
prep = ProposalsRepository()

controller = Controller()


@run.route("/<string:key>")
@login_required
def index(key):
    session_entity = srep.get(key)
    return render_template("run_index.html", session=session_entity, key=session_entity["_id"])


@run.route("/<string:key>/manage")
@login_required
def manage(key):
    session_entity = srep.get(key)
    return render_template("run_manage.html", session=session_entity, key=session_entity["_id"])


@channel.on("join")
def on_join_message(json):
    room = json.get("room")
    controller.connect(request.sid, current_user.get_id(), room)


@channel.on("chat")
def on_chat_message(json):
    room = controller.room_of(request.sid)
    emit("chat", {
        "who": current_user.name,
        "msg": json.get("msg", None)
    }, room=room)


@channel.on("disconnect")
def on_disconnect():
    controller.disconnect(request.sid)


@channel.on("next")
def on_next_message(json):
    session_id = json.get("session")
    step = json.get("step")

    session = srep.get(session_id)
    proposal_idx = session.get("proposal_idx", 0)
    proposal_idx += step

    if proposal_idx < 0:
        proposal_idx = 0

    if proposal_idx >= len(session["proposals"]):
        emit("stage", {"closed": True}, room=session_id)
        session["proposal_idx"] = proposal_idx
        srep.save(session)
    else:
        proposal = prep.get(session["proposals"][proposal_idx])
        session["proposal_idx"] = proposal_idx
        srep.save(session)

        emit("stage", {
            "proposal": { "title": proposal["title"], "content": proposal["content"]}},
            room=session_id)

    return {"success": True}
