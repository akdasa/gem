from flask import render_template

from gbcma.db.proposals import ProposalsRepository
from gbcma.db.sessions import SessionsRepository
from gbcma.web.app.auth import access_denied
from .sessions import Sessions


class SessionController:
    """Controller of the session blueprint"""

    def __init__(self):
        """Initializes new instance of the SessionController class."""
        self.__rooms = Sessions()
        self.__sessions = SessionsRepository()
        self.__proposals = ProposalsRepository()

    # Pages ------------------------------------------------------------------------------------------------------------

    def index(self, session_id, user, manage=False):
        """Renders index page of the session using specified ID
        :param session_id: Session Id
        :param user User
        :param manage: Is it a managing page?"""
        session = self.__sessions.get(session_id)
        template = "run_index.html" if not manage else "run_manage.html"
        if manage and not user.has_permission("run.manage"):
            return access_denied()
        return render_template(template, session=session)

    # Messages ---------------------------------------------------------------------------------------------------------

    def join(self, socket_id, user, data):
        """Joins user (using socket_id and user_id to identification) to specified room.
        :param socket_id: SocketIO Id
        :param user: User
        :param data: Request data"""
        room = data.get("room")
        self.__rooms.connect(socket_id, user.get_id(), room)

    def chat(self, socket_id, user, data):
        """On chat message received.
        :param socket_id: SocketIO Id
        :param user: User
        :param data: Request data"""
        room = self.__rooms.room_of(socket_id)
        room.notify_chat(user, data.get("msg", None))

    def next(self, socket_id, data):
        """On next stage command received.
        :param socket_id: SocketIO Id
        :param data: Data"""
        room = self.__rooms.room_of(socket_id)
        return room.next(data)

    def disconnect(self, socket_id):
        """On user disconnected.
        :param socket_id:  SocketIO Id"""
        self.__rooms.disconnect(socket_id)
