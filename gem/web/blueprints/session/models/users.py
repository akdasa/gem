from gem.db import users
from gem.event import Event
from gem.web.app.auth import User


class SessionUsers:
    def __init__(self, session):
        """
        Initializes new instance of the SessionUsers class.
        :param session: Session
        """
        self.__session = session
        self.__users = {}
        self.__changed = Event()

    @property
    def changed(self):
        return self.__changed

    @property
    def all(self):
        return self.__users.values()

    def join(self, user_id):
        user = User(users.get(user_id))
        self.__users[user_id] = self.__map(user)
        self.__notify_changes()
        self.__session.notify("user", self.__map_json(user), room=user_id)
        self.__changed.notify(user_id, user, True)

    def leave(self, user_id):
        if user_id in self.__users:
            del self.__users[user_id]
        self.__notify_changes()
        #self.__changed.notify(user_id, user, False)

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
