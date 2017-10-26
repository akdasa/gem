from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from flask_socketio import emit

from gbcma.channel.channel import get
from gbcma.db.sessions import SessionsRepository
from gbcma.web.blueprints.run.controller import Controller

run = Blueprint("run", __name__, template_folder=".")
channel = get()
srep = SessionsRepository()

controller = Controller()


@run.route("/<string:key>")
@login_required
def index(key):
    session_entity = srep.get(key)
    return render_template("run_index.html", session=session_entity, key=session_entity["_id"])


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
    pass


@channel.on("disconnect")
def test_disconnect():
    #if current_user.name in clients:
    #    clients[current_user.name].remove(request.sid)
    #    if len(clients[current_user.name]) == 0:
    #        del clients[current_user.name]
    controller.disconnect(request.sid)



@channel.on('next')
def handle_my_custom_event(json):
    s123 = srep.get(json["key"])
    s123["_id"] = str(s123["_id"])
    print(s123)
    return s123
