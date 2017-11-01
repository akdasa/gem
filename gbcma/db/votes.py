from gbcma.db.repository import Repository
from .config import votes


class VotesRepository(Repository):
    """Provides interface for Votes collection of database."""

    def __init__(self):
        super().__init__(votes)

    def create(self, proposal_id):
        inserted_id = self._c.insert_one({
            "proposal_id": proposal_id
        }).inserted_id
        return self.get(inserted_id)