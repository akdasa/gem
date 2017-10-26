from gbcma.db.users import UsersRepository


class Room:
    def __init__(self):
        """Initializes new instance of the Room class."""
        self.__repository = UsersRepository()
        self.__sessions = {}

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
        self.__sessions[session_id] = Room.__map_db(user)

    def leave(self, session_id):
        if session_id in self.__sessions:
            del self.__sessions[session_id]

    @staticmethod
    def __map_db(user):
        return {
            "id": str(user["_id"]),
            "name": user["name"]
        }
