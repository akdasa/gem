from gbcma.db.repository import Repository
from .config import proposals


class ProposalsRepository(Repository):
    """Provides interface for Proposals collection of database."""

    def __init__(self):
        super().__init__(proposals)

    def search_by_title(self, term):
        return self._c.search({"title": {"$regex": term, "$options": "i"}})

    def create(self, title, content=None):
        return self._c.insert_one({
            "title": title,
            "content": content
        })
