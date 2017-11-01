from flask_socketio import join_room

from .models.session import Session


class Sessions:
    def __init__(self):
        self.__rooms = {}

    def room_of(self, session_id):
        for room_name in self.__rooms:
            room = self.__rooms[room_name]
            if room.users.is_socket_connected(session_id):
                return self.__rooms[room_name]

    def connect(self, socket_id, user_id, room):
        if room not in self.__rooms:
            self.__rooms[room] = Session(room)
        join_room(room, socket_id)
        self.__rooms[room].users.join(socket_id, user_id)

    def disconnect(self, socket_id):
        for room in self.__rooms:
            self.__rooms[room].users.leave(socket_id)
