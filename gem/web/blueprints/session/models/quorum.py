from random import randint, sample

from gem.db import users


class SessionQuorum:
    def __init__(self, session):
        self.__session = session
        self.__value = 19
        self.__new_value = None
        self.__codes = []

    @property
    def value(self):
        return self.__value

    def request_change(self, value):
        self.__new_value = value
        users = self.__get_online_users_can_change()
        self.__generate_codes(len(users))

        for idx, user in enumerate(users):
            code = self.__codes[idx]
            self.__session.notify("quorum_change_code", {"code": code}, room=str(user.id))

        return {"users": self.__user_names(users)}

    def change(self, codes):
        codes_match = sorted(self.__codes) == sorted(codes)

        if codes_match:
            self.__value = self.__new_value
            return {"success": True, "message": "Quorum changed to {}".format(self.__value), "value": self.__value}
        else:
            return {"success": False, "message": "Codes doesn't match"}

    def __generate_codes(self, count):
        self.__codes.clear()
        for i in range(0, count):
            code = randint(100, 999)
            self.__codes.append(code)

    def __get_online_users_can_change(self):
        # get list of users can change quorum
        users_can_change = users.with_permission("quorum.change")

        # gets connections for users
        connections = {str(user.id): self.__session.connections.find(user_id=str(user.id)) for user in users_can_change}

        # get online users. filter out users with no connection
        online = {user_id: connections for user_id, connections in connections.items() if len(connections) > 0}
        online = list(map(lambda x: users.get(x), online.keys()))

        # return list of users (max 3)
        count_to_choose = min(3, len(online))
        return sample(online, count_to_choose)

    @staticmethod
    def __user_names(users):
        return list(map(lambda x: x.name, users))
