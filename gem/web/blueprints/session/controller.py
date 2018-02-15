from flask import render_template

from gem.db import sessions, proposals
from gem.web.app.auth import access_denied
from gem.web.app.sockets import disconnect_socket
from .models.session import Session
from .connections import Connections


class SessionController:
    """Controller of the session blueprint"""

    def __init__(self):
        """Initializes new instance of the SessionController class."""
        self.__connections = Connections()
        self.__connections.open_session.subscribe(self.__open_session)

    # Pages ------------------------------------------------------------------------------------------------------------

    def index(self, session_id, user):
        """Renders index page of the session using specified ID
        :param session_id: Session Id
        :param user User"""
        session_doc = sessions.get(session_id)

        # check the permissions
        if not session_doc:
            return access_denied("No session found")
        if not user.has_permission("session.join"):
            return access_denied()
        if session_doc.get("status", None) != "run":
            return access_denied("Session is not started yet or closed")
        if user.role not in session_doc["permissions"]["presence"]:
            return access_denied("You have no rights to join this session")

        # fetch additional data
        proposal_docs = proposals.find({"_id": {"$in": session_doc.proposals}})
        proposal_map = {
            str(proposal.id): {"title": proposal.title, "content": proposal.content, "id": proposal.id, "state": proposal.state} for proposal in proposal_docs
        }

        # view
        template = "session_presenter.html" if user.has_permission("presenter") else "session_index.html"

        return render_template(template, session=session_doc, proposals=proposal_map)

    # Messages ---------------------------------------------------------------------------------------------------------

    def join(self, socket_id, user_id, data):
        """Joins user (using socket_id and user for identification) to specified session.
        :param socket_id: SocketIO Id
        :param user_id: User Id
        :param data: Request data"""
        session_id = data.get("session", None)
        if session_id:  # session id is provided
            self.__connections.add(socket_id, user_id, session_id)
            return {"success": True}
        return {"success": False}

    def chat(self, socket_id, data):
        """On chat message received.
        :param socket_id: SocketIO Id
        :param user: User
        :param data: Request data"""
        cd = self.__connections.of_socket(socket_id)
        cd.session.chat.say(cd.user, data.get("msg", None))

    def change_stage(self, socket_id, data):
        """On next stage command received.
        :param socket_id: SocketIO Id
        :param data: Data"""
        cd = self.__connections.of_socket(socket_id)
        direction = data.get("value", 0)
        return cd.session.stages.change(direction)

    def vote(self, socket_id, data):
        """On vote command received.
        :param socket_id: SocketIO Id
        :param data: Data"""
        cd = self.__connections.of_socket(socket_id)
        vote_value = data.get("value", None)
        return cd.session.stages.current.vote(cd.user, vote_value)

    def comment(self, socket_id, data):
        """On comment command received.
        :param socket_id: SocketIO Id
        :param user: User
        :param data: Data"""
        cd = self.__connections.of_socket(socket_id)
        content = data.get("content", None)
        kind = data.get("type", None)
        quote = data.get("quote", None)
        return cd.session.stages.current.comment(cd.user, content, kind, quote)

    def set_timer(self, socket_id, data):
        minutes = data.get("interval", 1)
        cd = self.__connections.of_socket(socket_id)
        return cd.session.notify("timer", {"interval": minutes})

    def manage(self, socket_id, data):
        cd = self.__connections.of_socket(socket_id)
        return cd.session.stages.current.manage(data, user=cd.user)

    def manage_session(self, socket_id, data):
        cd = self.__connections.of_socket(socket_id)
        return cd.session.manage(data, cd.user)

    def close(self, socket_id):
        """On close stage command received.
        :param socket_id: SocketIO Id"""
        cd = self.__connections.of_socket(socket_id)

        # disconnect all active clients
        active = self.__connections.of_session(cd.session_id)
        for acd in active:
            if acd.socket_id == cd.socket_id:
                continue
            acd.session.notify("kick", {"message": "Session is closed", "title": "Closed"}, room=acd.socket_id)

        return cd.session.close()

    def disconnect(self, socket_id):
        """On user disconnected.
        :param socket_id:  SocketIO Id"""
        self.__connections.remove(socket_id)

    def kick(self, socket_id, data):
        user_id = data.get("user", None)  # user id to kick
        reason = data.get("reason", None) # reason

        cds = self.__connections.of_user(user_id)
        for cd in cds:
            cd.session.notify("kick", {"message": reason}, room=cd.socket_id)
            disconnect_socket(cd.socket_id)

    def __open_session(self, session_id):
        return Session(session_id, self.__connections)
