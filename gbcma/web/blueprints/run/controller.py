from flask_socketio import join_room, emit

from .models import Room


class Controller():
    def __init__(self):
        self.__rooms = {}

    def room_of(self, session_id):
        for room_name in self.__rooms:
            room = self.__rooms[room_name]
            if room.is_session_connected(session_id):
                return room_name

    def connect(self, session_id, user_id, room):
        if room not in self.__rooms:
            self.__rooms[room] = Room()
        self.__rooms[room].join(session_id, user_id)
        join_room(room, session_id)
        self.__notify_user_changes(room)

    def disconnect(self, session_id):
        for room in self.__rooms:
            self.__rooms[room].leave(session_id)
            self.__notify_user_changes(room)

    def __notify_user_changes(self, room):
        r = self.__rooms[room]
        emit("users", r.users, room=room)