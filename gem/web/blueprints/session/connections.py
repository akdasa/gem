from collections import namedtuple

from flask_socketio import join_room

from gem.db import users
from .models.session import Session


ConnectionData = namedtuple("ConnectionData", ["user_id", "socket_id", "session_id", "session", "user"])


class Connections:
    def __init__(self):
        self.__rooms = {}
        self.__connections = []

    def find(self, user_id=None, socket_id=None, session_id=None):
        if user_id:
            return list(filter(lambda x: x.user_id == user_id, self.__connections))
        elif socket_id:
            return (list(filter(lambda x: x.socket_id == socket_id, self.__connections)) or [None])[0]
        elif session_id:
            return filter(lambda x: x.session_id == session_id, self.__connections)
        else:
            raise Exception("No filter provided")

    def add(self, socket_id, user_id, session_id):
        # Create new session controller if not exist
        if session_id not in self.__rooms:
            self.__rooms[session_id] = Session(session_id, self)

        join_room(session_id, socket_id)
        join_room(user_id, socket_id)

        user = users.get(user_id)
        session = self.__rooms[session_id]
        cd = ConnectionData(user_id, socket_id, session_id, session, user)
        self.__connections.append(cd)
        session.users.join(user_id)

    def remove(self, socket_id):
        cd = self.find(socket_id=socket_id)
        cd.session.users.leave(cd.user_id)
        self.__connections.remove(cd)
