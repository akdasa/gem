from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, dict):
        print("DDD", dict)
        self.__id = str(dict["_id"])
        self.__name = dict.get("name", "<Noname das>")
        self.__roles = dict.get("roles", [])

    def get_id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def roles(self):
        return self.__roles

    def has_role(self, name):
        return name in self.__roles
