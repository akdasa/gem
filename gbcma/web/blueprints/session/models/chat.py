class SessionChat:
    def __init__(self, session):
        self.__session = session

    def say(self, user, message):
        self.__session.notify("chat", {
            "who": user.name,
            "msg": message
        })