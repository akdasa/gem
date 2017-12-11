from bson import ObjectId
from bson.errors import InvalidId
from .model import Model


class Repository:
    def __init__(self, collection):
        """Initializes new instance of the Repository class."""
        self._collection = collection

    def all(self):
        """Returns all items in collection.
        :return: Array of items."""
        return self.__map(list(self._collection.find()))

    def get(self, oid):
        try:
            return self.__map(self._collection.find_one(ObjectId(oid)))
        except InvalidId:
            return None

    def get_list(self, oids):
        return self.__map(list(self.find({"_id": {"$in": oids}})))

    def find_one(self, criteria):
        try:
            return self.__map(self._collection.find_one(criteria))
        except InvalidId:
            return None

    def find(self, criteria):
        return self.__map(list(self._collection.find(criteria)))

    def insert(self, doc):
        return self._collection.insert_one(doc)

    def save(self, doc):
        return self._collection.replace_one(
            {"_id": doc["_id"]}, doc)

    def delete(self, key):
        return self._collection.find_one_and_delete({
            "_id": ObjectId(key)
        })

    def __map(self, data):
        if data is None:
            return None
        elif type(data) is list:
            return list(map(lambda x: Model(**x), data))
        else:
            return Model(**data)
