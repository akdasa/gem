from .config import proposals


class ProposalsRepository:
    """Provides interface for Proposals collection of database."""

    def __init__(self, collection=None):
        self.__collection = collection or proposals

    def get(self, key):
        return self.__collection.find_one({"key": key})

    def find(self):
        return self.__collection.find()

    def create(self, key, title, content=None):
        return self.__collection.insert_one({
            "key": key,
            "title": title,
            "content": content
        })
