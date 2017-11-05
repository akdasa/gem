from bson import ObjectId

from gbcma.db.repository import Repository
from .config import votes


class VotesRepository(Repository):
    """Provides interface for Votes collection of database."""

    def __init__(self):
        super().__init__(votes)

    def find_or_create(self, proposal_id):
        doc = self._c.find_one({"proposal_id": ObjectId(proposal_id)})
        if not doc:
            doc = self.create(proposal_id)
        return doc

    def create(self, proposal_id):
        inserted_id = self._c.insert_one({
            "proposal_id": proposal_id,
            "votes": {}
        }).inserted_id
        return self.get(inserted_id)
