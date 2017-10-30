from bson import ObjectId
from bson.errors import InvalidId


class Repository:
    def __init__(self, collection):
        self._c = collection

    def all(self):
        return self._c.find()

    def get(self, key):
        try:
            return self._c.find_one(ObjectId(key))
        except InvalidId:
            return None

    def find(self, criteria):
        try:
            return self._c.find_one(criteria)
        except InvalidId:
            return None

    def search(self, criteria):
        return self._c.find(criteria)

    def insert(self, doc):
        return self._c.insert_one(doc)

    def save(self, doc):
        return self._c.replace_one(
            {"_id": doc["_id"]}, doc)

    def delete(self, key):
        return self._c.find_one_and_delete({
            "_id": ObjectId(key)
        })
