from bson import ObjectId


class Repository:
    def __init__(self, collection):
        self.__collection = collection

    def all(self):
        return self.__collection.find()

    def get(self, key):
        return self.__collection.find_one(ObjectId(key))

    def find(self, criteria):
        return self.__collection.find_one(criteria)

    def insert(self, doc):
        return self.__collection.insert_one(doc)

    def save(self, doc):
        return self.__collection.replace_one(
            {"_id": doc["_id"]}, doc)

    def delete(self, key):
        return self.__collection.find_one_and_delete({
            "_id": ObjectId(key)
        })
