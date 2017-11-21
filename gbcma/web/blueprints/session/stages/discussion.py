from gbcma.db import users
from .stage import SessionStage


class DiscussionSessionStage(SessionStage):
    """Represents one stage of the Session."""

    def __init__(self, session, proposal):
        super().__init__(session, proposal)
        self.__queue = {}
        self.__speaking = None

    @property
    def view(self):
        """Returns JSON representation of the stage"""
        return {
            "speaking": self.__speaking,
            "queue": list(map(lambda x: self.__queue[x], self.__queue))
        }

    def raise_hand(self, user):
        if self.__is_user_raised_hand(user):
            return

        self.__queue[user.id] = ({
            "id": user.id,
            "name": user.name,
            "order": len(self.__queue)
        })
        self.changed.notify()

    def withdraw_hand(self, user):
        if not self.__is_user_raised_hand(user):
            return

        if self.__speaking and self.__speaking["id"] == user.id:
            self.__speaking = None

        del self.__queue[user.id]

        self.changed.notify()

    def give_voice(self, user_id):
        user = users.get(user_id)
        if user:
            self.__speaking = {
                "id": user_id,
                "name": user["name"]
            }
        self.changed.notify()

    def __is_user_raised_hand(self, user):
        ids = map(lambda x: self.__queue[x]["id"], self.__queue)
        return user.id in ids
