from gem.event import Event
from gem.web.app.auth import User


class SessionUsers:
    def __init__(self, session):
        """
        Initializes new instance of the SessionUsers class.
        :param session: Session
        """
        self.__session = session
        self.__sockets = {}  # multiple sockets per one user is possible
        self.__changed = Event()

    @property
    def changed(self):
        """
        On users changed
        :return: Event
        """
        return self.__changed

    @property
    def all(self):
        result = []
        ids_present = []
        users = self.__sockets.values()
        for user in users:
            user_id = user.get_id()
            if user_id not in ids_present:
                result.append(user)
                ids_present.append(user_id)
        return result

    def is_present(self, user):
        for u in self.all:
            if u.get_id() == user.id:
                return True
        return False

    def join(self, socket_id, user):
        self.__sockets[socket_id] = self.__map(user)
        self.__notify_changes()
        self.__session.notify("user", self.__map_json(user), room=socket_id)
        self.__changed.notify(socket_id, user, True)

    def leave(self, socket_id):
        if socket_id not in self.__sockets:
            return

        user = self.__sockets[socket_id]
        del self.__sockets[socket_id]
        self.__notify_changes()
        self.__changed.notify(socket_id, user, False)

    def __notify_changes(self):
        users = list(map(lambda x: {"name": x.name, "role": x.role, "id": x.id}, self.all))
        self.__session.notify("users", users)

    @staticmethod
    def __map(user, json=False):
        return User({
            "_id": user.id if not json else str(user.id),
            "name": user.name,
            "permissions": user.permissions,
            "role": user.role
        })

    def __map_json(self, user):
        can_present = user.role in self.__session.presence_roles
        can_vote = (user.role in self.__session.vote_roles) and \
                   ("vote" in user.permissions)

        permissions = list(user.permissions)
        if permissions:
            if "vote" in permissions and not can_vote:
                permissions.remove("vote")
            if "session.join" in permissions and not can_present:
                permissions.remove("session.join")

        return {
            "_id": str(user.id),
            "name": user.name,
            "permissions": permissions,
            "role": user.role,
        }
