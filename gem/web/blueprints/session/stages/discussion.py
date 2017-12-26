from gem.db import users
from .stage import SessionStage


class DiscussionSessionStage(SessionStage):
    """Represents discussion stage of the Session."""

    def __init__(self, session, proposal):
        """Initializes new instance of the SessionStage class.
        :type session: Session
        :type proposal: Proposal
        :param session: Session to which the stage belongs
        :param proposal: Proposal document"""
        super().__init__(session, proposal)
        self.__queue = {}
        self.__speaking = None
        self.__order = 0
        self.__accept = True

    def manage(self, data, user=None):
        cmd = data.get("command", None)

        if cmd == "raise_hand":
            self.__raise_hand(user)
        if cmd == "withdraw_hand":
            self.__withdraw_hand(user)
        if cmd == "give_voice":
            self.__give_voice(data["user_id"])
        if cmd == "accept":
            self.__accept = data.get("value", True)
            self.changed.notify()

    def __raise_hand(self, user):
        """User raises a hand.
        :type user: User
        :param user: User"""
        if self.__is_raised_hand(user):
            return
        if not self.__accept:
            return

        self.__order += 1
        self.__queue[user.id] = ({
            "id": user.id,
            "name": user.name,
            "role": user.role,
            "order": self.__order
        })
        self.changed.notify()

    def __withdraw_hand(self, user):
        """User withdraws a hand.
        :param user: User"""
        if not self.__is_raised_hand(user):
            return

        if self.__speaking and self.__speaking["id"] == user.id:
            self.__speaking = None
        del self.__queue[user.id]
        self.changed.notify()

    def __give_voice(self, user_id):
        """Give a voice for specified user.
        :param user_id: User's id"""
        user = users.get(user_id)
        if user:
            self.__speaking = {
                "id": user_id,
                "name": user.name
            }
        self.changed.notify()

    @property
    def view(self):
        """Returns JSON representation of the stage"""
        return {
            "speaking": self.__speaking,
            "accept": self.__accept,
            "queue": list(map(lambda x: self.__queue[x], self.__queue))
        }

    def __is_raised_hand(self, user):
        return user.id in self.__queue
