from flask_socketio import join_room

from gem.db import users
from .models.session import Session


class SocketSessions:
    def __init__(self):
        self.__rooms = {}
        self.__by_room = {}
        self.__socket_id = {}
        self.__user_id = {}

    def get_socket_id(self, user_id):
        return self.__socket_id.get(user_id, None)

    def session_of(self, socket_id):
        return self.__by_room[socket_id]

    def user_of(self, socket_id):
        user_id = self.__user_id.get(socket_id, None)
        if user_id:
            return users.get(user_id)
        return None

    def connect(self, socket_id, user_id, session_id):
        # Create new session controller if not exist
        if session_id not in self.__rooms:
            self.__rooms[session_id] = Session(session_id)

        join_room(session_id, socket_id)
        join_room(user_id, socket_id)
        self.__rooms[session_id].users.join(user_id)
        self.__by_room[socket_id] = self.__rooms[session_id]
        self.__socket_id[user_id] = socket_id
        self.__user_id[socket_id] = user_id

    def disconnect(self, socket_id):
        if socket_id in self.__by_room:
            user_id = self.__user_id[socket_id]
            self.__by_room[socket_id].users.leave(user_id)
