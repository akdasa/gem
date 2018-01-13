from random import randint

from gem.db import users


class SessionQuorum:
    def __init__(self, session):
        self.__session = session
        self.__value = 19
        self.__new_value = None
        self.__codes = []

    def request_change(self, value):
        self.__new_value = value
        users = self.__get_persons()
        self.__generate_codes(len(users))

        for idx, user in enumerate(users):
            code = self.__codes[idx]
            self.__session.notify("quorum_change_code", {"code": code}, room=str(user.id))

        return {"users": self.__user_names(users)}

    def change(self, codes):
        codes_match = sorted(self.__codes) == sorted(codes)

        if codes_match:
            self.__value = self.__new_value
            return {"success": True, "message": "Quorum changed to {}".format(self.__value)}
        else:
            return {"success": False, "message": "Codes doesn't match"}

    def __generate_codes(self, count):
        self.__codes.clear()
        for i in range(0, count):
            code = randint(100, 999)
            self.__codes.append(code)

    @staticmethod
    def __get_persons():
        return users.with_permission("quorum.change")

    @staticmethod
    def __user_names(users):
        return list(map(lambda x: x.name, users))
