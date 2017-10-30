from flask_socketio import emit

from gbcma.db.proposals import ProposalsRepository
from gbcma.db.sessions import SessionsRepository
from gbcma.db.users import UsersRepository


class Session:
    def __init__(self, name):
        """Initializes new instance of the Session class."""
        self.__name = name
        self.__repository = UsersRepository()
        self.__sessions = {}
        self.__srep = SessionsRepository()
        self.__prep = ProposalsRepository()

    @property
    def sessions(self):
        """
        Returns list of session ids connected to this room.
        :return: Array of ids.
        """
        return list(self.__sessions.values())

    @property
    def users(self):
        """
        Returns list of user ids joined this room.
        :return: Array of ids.
        """
        result = []
        ids_present = []
        users = self.__sessions.values()
        for user in users:
            user_id = user["id"]
            if user_id not in ids_present:
                result.append(user)
                ids_present.append(user_id)
        return result

    def is_session_connected(self, session_id):
        return session_id in self.__sessions

    def join(self, session_id, user_id):
        user = self.__repository.get(user_id)
        self.__sessions[session_id] = Session.__map_db(user)
        self.notify_user_changes()
        self.notify_stage(session_id)

    def leave(self, session_id):
        if session_id in self.__sessions:
            del self.__sessions[session_id]
            self.notify_user_changes()

    def notify_user_changes(self):
        emit("users", self.users, room=self.__name)

    def notify_stage(self, room=None):
        who = self.__name if room is None else room
        emit("stage", self.__session_stage(), room=who)

    def notify_chat(self, user, message):
        emit("chat", {
            "who": user.name,
            "msg": message
        }, room=self.__name)

    def next(self, data):
        session_id = self.__name #data.get("session")
        step = data.get("step")

        session = self.__srep.get(session_id)
        proposal_idx = session.get("proposal_idx", 0)
        proposal_idx += step

        if proposal_idx < 0:
            proposal_idx = 0

        if proposal_idx >= len(session["proposals"]):
            emit("stage", {"closed": True}, room=session_id)
            session["proposal_idx"] = proposal_idx
            self.__srep.save(session)
        else:
            proposal = self.__prep.get(session["proposals"][proposal_idx])
            session["proposal_idx"] = proposal_idx
            self.__srep.save(session)

            emit("stage", {
                "proposal": {"title": proposal["title"], "content": proposal["content"]}},
                 room=session_id)

        return {"success": True}

    def __session_stage(self):
        session = self.__srep.get(self.__name)
        proposal_idx = session.get("proposal_idx", 0)

        if proposal_idx >= len(session["proposals"]):
            return {"closed": True}
        else:
            proposal = self.__prep.get(session["proposals"][proposal_idx])
            return {"proposal": {"title": proposal["title"], "content": proposal["content"]}}

    @staticmethod
    def __map_db(user):
        return {
            "id": str(user["_id"]),
            "name": user["name"]
        }
