class SessionChat:
    """Chat aspect of session"""

    def __init__(self, session):
        """
        Initializes new instance of the SessionChat class.
        :type session: Session
        :param session: Session.
        """
        self.__session = session

    def say(self, user, message):
        """
        Say.
        :type user: User
        :type message: str
        :param user: User
        :param message: Message
        """
        self.__session.notify("chat", {
            "who": user.name,
            "msg": message
        })
