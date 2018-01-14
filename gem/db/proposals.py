from gem.db.core.model import Model
from .config import proposals
from .core import Repository


class Proposal(Model):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not hasattr(self, "state"):
            self.state = "new"


class ProposalsRepository(Repository):
    """Provides interface for Proposals collection of database."""

    def __init__(self):
        super().__init__(proposals, cls=Proposal)

    def search_by_title(self, term):
        return self.find({"title": {"$regex": term, "$options": "i"}})

    def create(self, title, content=None):
        return self._collection.insert_one({
            "title": title,
            "content": content
        })
