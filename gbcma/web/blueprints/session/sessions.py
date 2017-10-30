from flask_socketio import join_room, emit

from .session import Session


class Sessions:
    def __init__(self):
        self.__rooms = {}

    def room_of(self, session_id):
        for room_name in self.__rooms:
            room = self.__rooms[room_name]
            if room.is_session_connected(session_id):
                return self.__rooms[room_name]

    def connect(self, session_id, user_id, room):
        if room not in self.__rooms:
            self.__rooms[room] = Session(room)
        join_room(room, session_id)
        self.__rooms[room].join(session_id, user_id)

    def disconnect(self, session_id):
        for room in self.__rooms:
            self.__rooms[room].leave(session_id)
