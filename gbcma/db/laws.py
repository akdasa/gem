from .core import Repository
from .config import laws


class LawsRepository(Repository):
    """Provides interface for Laws collection of database."""

    def __init__(self):
        super().__init__(laws)

    def search_by_title(self, term):
        return self.find({"title": {"$regex": term, "$options": "i"}})

    def create(self, key, title, content=None):
        return self._collection.insert_one({
            "key": key,
            "title": title,
            "content": content
        })
