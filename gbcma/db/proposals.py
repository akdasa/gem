from gbcma.db.repository import Repository
from .config import proposals


class ProposalsRepository(Repository):
    """Provides interface for Proposals collection of database."""

    def __init__(self):
        super().__init__(proposals)

    def create(self, title, content=None):
        return self.__collection.insert_one({
            "title": title,
            "content": content
        })
