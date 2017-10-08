from bson import ObjectId

from .config import proposals


class ProposalsRepository:
    """Provides interface for Proposals collection of database."""

    def __init__(self, collection=None):
        self.__collection = collection or proposals

    def get(self, key):
        return self.__collection.find_one(ObjectId(key))

    def find(self):
        return self.__collection.find()

    def create(self, title, content=None):
        return self.__collection.insert_one({
            "title": title,
            "content": content
        })

    def save(self, proposal):
        return self.__collection.replace_one(
            {"_id": proposal["_id"]}, proposal)
