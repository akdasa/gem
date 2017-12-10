from flask import render_template

from gbcma.db import sessions
from gbcma.web.app.auth import access_denied
from .socket_sessions import SocketSessions


class SessionController:
    """Controller of the session blueprint"""

    def __init__(self):
        """Initializes new instance of the SessionController class."""
        self.__sockets = SocketSessions()

    # Pages ------------------------------------------------------------------------------------------------------------

    def index(self, session_id, user, manage=False):
        """Renders index page of the session using specified ID
        :param session_id: Session Id
        :param user User
        :param manage: Is it a managing page?"""
        template = "session_index.html" if not manage else "session_manage.html"
        session = sessions.get(session_id)
        if not session:
            return access_denied("No session found")
        if not manage and not user.has_permission("session.join"):
            return access_denied()
        if manage and not user.has_permission("session.manage"):
            return access_denied()
        if session.get("status", None) != "run":
            return access_denied("Session is not started yet or closed")
        if user.role not in session["permissions"]["presence"]:
            return access_denied("You have no rights to join this session")

        return render_template(template, session=session)

    # Messages ---------------------------------------------------------------------------------------------------------

    def join(self, socket_id, user, data):
        """Joins user (using socket_id and user for identification) to specified session.
        :param socket_id: SocketIO Id
        :param user: User
        :param data: Request data"""
        session_id = data.get("room")
        self.__sockets.connect(socket_id, user, session_id)

    def chat(self, socket_id, user, data):
        """On chat message received.
        :param socket_id: SocketIO Id
        :param user: User
        :param data: Request data"""
        session = self.__sockets.session_of(socket_id)
        session.chat.say(user, data.get("msg", None))

    def change_stage(self, socket_id, data):
        """On next stage command received.
        :param socket_id: SocketIO Id
        :param data: Data"""
        session = self.__sockets.session_of(socket_id)
        direction = data.get("value", 0)
        return session.stages.change(direction)

    def vote(self, socket_id, user, data):
        """On vote command received.
        :param socket_id: SocketIO Id
        :param user: User
        :param data: Data"""
        session = self.__sockets.session_of(socket_id)
        vote_value = data.get("value", None)
        return session.stages.current.vote(user, vote_value)

    def comment(self, socket_id, user, data):
        """On comment command received.
        :param socket_id: SocketIO Id
        :param user: User
        :param data: Data"""
        session = self.__sockets.session_of(socket_id)
        content = data.get("content", None)
        kind = data.get("type", None)
        quote = data.get("quote", None)
        return session.stages.current.comment(user, content, kind, quote)

    def raise_hand(self, socket_id, user, data):
        """On raise hand command received.
        :param socket_id: SocketIO Id
        :param user: User
        :param data: Data"""
        session = self.__sockets.session_of(socket_id)
        return session.stages.current.raise_hand(user)

    def withdraw_hand(self, socket_id, user, data):
        """On withdraw hand command received.
        :param socket_id: SocketIO Id
        :param user: User
        :param data: Data"""
        session = self.__sockets.session_of(socket_id)
        return session.stages.current.withdraw_hand(user)

    def give_voice(self, socket_id, user, data):
        """On give voice command received.
        :param socket_id: SocketIO Id
        :param user: User
        :param data: Data"""
        session = self.__sockets.session_of(socket_id)
        to_user_id = data.get("user_id", None)
        return session.stages.current.give_voice(to_user_id)

    def set_timer(self, socket_id, data):
        minutes = data.get("interval", 1)
        session = self.__sockets.session_of(socket_id)
        return session.notify("timer", {"interval": minutes})

    def close(self, socket_id):
        """On close stage command received.
        :param socket_id: SocketIO Id"""
        session = self.__sockets.session_of(socket_id)
        return session.close()

    def disconnect(self, socket_id):
        """On user disconnected.
        :param socket_id:  SocketIO Id"""
        self.__sockets.disconnect(socket_id)
