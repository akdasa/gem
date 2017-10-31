from flask_socketio import emit

from gbcma.db.proposals import ProposalsRepository
from gbcma.db.sessions import SessionsRepository


class Session:
    def __init__(self, name):
        """Initializes new instance of the Session class."""
        self.__name = name
        self.__sockets = {}
        self.__load(name)

    # @property
    # def sessions(self):
    #     """Returns list of session ids connected to this room.
    #     :return: Array of ids."""
    #     return list(self.__sessions.values())

    @property
    def users(self):
        """Returns list of user ids joined this room.
        :return: Array of ids."""
        result = []
        ids_present = []
        users = self.__sockets.values()
        for user in users:
            user_id = user["id"]
            if user_id not in ids_present:
                result.append(user)
                ids_present.append(user_id)
        return result

    @property
    def proposal_idx(self):
        return self.__entity.get("proposal_idx", 0)

    @proposal_idx.setter
    def proposal_idx(self, value):
        self.__entity["proposal_idx"] = value

    @property
    def proposals_count(self):
        return len(self.__entity["proposals"])

    @property
    def state(self):
        return self.__entity["status"]

    @state.setter
    def state(self, value):
        self.__entity["status"] = value

    def is_socket_connected(self, socket_id):
        return socket_id in self.__sockets

    def join(self, socket_id, user):
        self.__sockets[socket_id] = Session.__map_db(user)
        self.notify_user_changes()
        self.notify_stage(socket_id)

    def leave(self, socket_id):
        if socket_id in self.__sockets:
            del self.__sockets[socket_id]
            self.notify_user_changes()

    def notify_user_changes(self):
        emit("users", self.users, room=self.__name)

    def notify_stage(self, who=None):
        emit("stage", self.__state(), room=self.__name or who)

    def notify_chat(self, user, message):
        emit("chat", {
            "who": user.name,
            "msg": message
        }, room=self.__name)

    def next(self, data):
        self.proposal_idx += data.get("step", 1)
        if self.proposal_idx < 0:
            self.proposal_idx = 0
        if self.proposal_idx >= self.proposals_count:
            self.proposal_idx = self.proposals_count

        self.__save()
        emit("stage", self.__state(), room=self.__name)

    def close(self):
        self.state = "closed"
        self.__save()
        return {"state": self.state}

    def __state(self):
        """Return current state fo session.
        :return: Dictionary what represents current state of session"""
        proposal_idx = self.__entity.get("proposal_idx", 0)
        proposals_count = len(self.__entity["proposals"])

        if proposal_idx < proposals_count:
            proposal_key = self.__entity["proposals"][proposal_idx]
            proposal = self.__get_proposal(proposal_key)
            return {
                "proposal": {"title": proposal["title"], "content": proposal["content"]},
                "progress": {"current": self.proposal_idx+1, "total": self.proposals_count}}
        else:
            return {"closed": True}

    @staticmethod
    def __get_proposal(key):
        """Returns proposal by specified key
        :param key: Proposal Id
        :return: Proposal"""
        rep = ProposalsRepository()
        return rep.get(key)

    @staticmethod
    def __map_db(user):
        return {
            "id": str(user.get_id()),
            "name": user.name
        }

    def __load(self, key):
        rep = SessionsRepository()
        self.__entity = rep.get(key)

    def __save(self):
        rep = SessionsRepository()
        rep.save(self.__entity)
