import flask


def disconnect_socket(socket_id):
    socket_io = flask.current_app.extensions['socketio']
    socket_io.server.disconnect(socket_id)
