from flask_socketio import join_room

from .models.session import Session


class SocketSessions:
    def __init__(self):
        self.__rooms = {}
        self.__by_room = {}
        self.__socket_id = {}

    def get_session(self, session_id):
        return self.__rooms.get(session_id, None)

    def get_socket_id(self, user_id):
        return self.__socket_id.get(user_id, None)

    def session_of(self, socket_id):
        return self.__by_room[socket_id]

    def connect(self, socket_id, user, session_id):
        if session_id not in self.__rooms:
            self.__rooms[session_id] = Session(session_id)
        join_room(session_id, socket_id)
        self.__rooms[session_id].users.join(socket_id, user)
        self.__by_room[socket_id] = self.__rooms[session_id]
        self.__socket_id[user.id] = socket_id

    def disconnect(self, socket_id):
        if socket_id in self.__by_room:
            self.__by_room[socket_id].users.leave(socket_id)
