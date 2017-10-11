from bson import ObjectId

from .config import users


class UsersRepository:
    """Provides interface for Proposals collection of database."""

    def __init__(self, collection=None):
        self.__collection = collection or users

    def all(self):
        return self.__collection.find()

    def get(self, key):
        return self.__collection.find_one(ObjectId(key))

    def find(self, login, password):
        return self.__collection.find_one({"login": login, "password": password})

    def create(self, name, login, password, permissions=None):
        return self.__collection.insert_one({
            "name": name,
            "login": login,
            "password": password,
            "permissions": permissions
        })

    def save(self, proposal):
        return self.__collection.replace_one(
            {"_id": proposal["_id"]}, proposal)

    def delete(self, key):
        return self.__collection.find_one_and_delete({
            "_id": ObjectId(key)
        })
