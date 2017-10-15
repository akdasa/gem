from flask import Blueprint, render_template, jsonify, session, request
from flask_login import login_required, current_user
from flask_socketio import emit

from gbcma.channel.channel import get
from gbcma.db.sessions import SessionsRepository

run = Blueprint("run", __name__, template_folder=".")
channel = get()
clients = {}
srep = SessionsRepository()


@run.route("/<string:key>")
@login_required
def index(key):
    return render_template("run_index.html")


@run.route("/<string:key>/manage")
@login_required
def manage(key):
    return render_template("run_manage.html", key=key)


@channel.on('connect')
def test_connect():
    print("CONNECTED", request.sid)
    if current_user.name not in clients:
        clients[current_user.name] = []
    clients[current_user.name].append(request.sid)
    __notify_user_changes()


@channel.on('disconnect')
def test_disconnect():
    print("DIS---CONNECTED", request.sid)
    if current_user.name in clients:
        clients[current_user.name].remove(request.sid)
        if len(clients[current_user.name]) == 0:
            del clients[current_user.name]
    __notify_user_changes()



@channel.on('my event')
def handle_my_custom_event(json):
    return clients


@channel.on('chat')
def handle_my_custom_event(json):
    json["who"] = current_user.name
    emit("chat", json, broadcast=True)


@channel.on('next')
def handle_my_custom_event(json):
    s123 = srep.get(json["key"])
    s123["_id"] = str(s123["_id"])
    print(s123)
    return s123


def __notify_user_changes():
    emit("users", list(clients.keys()), broadcast=True)
