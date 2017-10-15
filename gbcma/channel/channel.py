from flask_socketio import SocketIO

_channel = None


def init(app):
    global _channel
    _channel = SocketIO(app)


def get():
    return _channel
