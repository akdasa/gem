from collections import namedtuple

from flask_socketio import join_room

from gem.db import users
from gem.event import Event

SessionConnection = namedtuple("SessionConnection", ["user_id", "socket_id", "session_id", "session", "user"])


class Connections:
    """
    Handles all the connections to the sessions.
    """

    def __init__(self):
        """
        Initializes new instance of the Connections class
        """
        self.__connections = []  # list of all connections
        self.__sessions = {}     # map of sessions: session_id -> Session model
        self.__open_session = Event()
        self.__close_session = Event()

    @property
    def open_session(self):
        """
        Fires then connection to new session established
        :rtype: Event
        :return: Event
        """
        return self.__open_session

    @property
    def close_session(self):
        """
        Fires then no connection to session remains
        :rtype: Event
        :return: Event
        """
        return self.__close_session

    def of_socket(self, socket_id):
        """Returns connection of specified socket
        :rtype: SessionConnection
        :type socket_id: str
        :param socket_id: Socket Id
        :return: Session connection data"""
        connections = list(filter(lambda x: x.socket_id == socket_id, self.__connections))
        if len(connections) > 0:
            return connections[0]
        return None

    def of_user(self, user_id):
        """Returns connection of specified socket
        :rtype: SessionConnection
        :type user_id: str
        :param user_id: User Id
        :return: List of connections data"""
        return list(filter(lambda x: x.user_id == user_id, self.__connections))

    def of_session(self, session_id):
        """Returns connection of specified socket
        :rtype: SessionConnection
        :type session_id: str
        :param session_id: Session Id
        :return: List of connections data"""
        return filter(lambda x: x.session_id == session_id, self.__connections)

    def add(self, socket_id, user_id, session_id):
        """Adds new connection using specified socket, user, session ids.
        :param socket_id: Socket Id
        :param user_id: User Id
        :param session_id: Session Id"""
        # Create new session controller if not exist
        if session_id not in self.__sessions:
            session = self.__open_session.notify(session_id)
            if len(session) <= 0:
                raise Exception("No session object created by open_session event handler")
            self.__sessions[session_id] = session[0]

        join_room(session_id, socket_id)
        join_room(user_id, socket_id)

        user = users.get(user_id)
        session = self.__sessions[session_id]
        cd = SessionConnection(user_id, socket_id, session_id, session, user)
        self.__connections.append(cd)
        session.users.join(user_id)

    def remove(self, socket_id):
        # find connection data for specified socket
        connection = self.of_socket(socket_id)
        if not connection:
            return

        # remove user from session, close session if no user remains
        connection.session.users.leave(connection.user_id)
        if len(connection.session.users.all) <= 0:
            if self.__close_session:
                self.__close_session.notify(connection.session)
            del self.__sessions[connection.session_id]

        # remove connection
        self.__connections.remove(connection)
