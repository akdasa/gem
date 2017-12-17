from bson import ObjectId

from gbcma.db.core.model import Model
from .config import votes
from .core import Repository


class VotesRepository(Repository):
    """Provides interface for Votes collection of database."""

    def __init__(self):
        super().__init__(votes)

    def find_or_create(self, proposal_id):
        doc = self._collection.find_one({"proposal_id": ObjectId(proposal_id)})
        if not doc:
            doc = self.create(proposal_id)
        return Model(**doc)

    def create(self, proposal_id):
        inserted_id = self._collection.insert_one({
            "proposal_id": proposal_id,
            "votes": {}
        }).inserted_id
        return self.get(inserted_id)
