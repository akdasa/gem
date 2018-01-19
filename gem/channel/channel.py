from flask_socketio import SocketIO
from flask import json

_channel = None


def init(app):
    global _channel
    _channel = SocketIO(app, json=json)


def get():
    return _channel
