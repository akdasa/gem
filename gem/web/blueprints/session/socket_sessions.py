from flask_socketio import join_room

from .models.session import Session


class SocketSessions:
    def __init__(self):
        self.__rooms = {}
        self.__by_room = {}

    def session_of(self, socket_id):
        return self.__by_room[socket_id]

    def connect(self, socket_id, user_id, room):
        if room not in self.__rooms:
            self.__rooms[room] = Session(room)
        join_room(room, socket_id)
        self.__rooms[room].users.join(socket_id, user_id)
        self.__by_room[socket_id] = self.__rooms[room]

    def disconnect(self, socket_id):
        self.__by_room[socket_id].users.leave(socket_id)
