from bson import ObjectId

from .core import Repository
from .config import comments


class CommentsRepository(Repository):
    """Provides interface for Comments collection of database."""

    def __init__(self):
        super().__init__(comments)

    def create(self, proposal_id, user_id, content, kind, quote=None):
        inserted_id = self._collection.insert_one({
            "proposal_id": ObjectId(proposal_id),
            "user_id": ObjectId(user_id),
            "content": content,
            "type": kind,
            "quote": quote
        }).inserted_id
        return self.get(inserted_id)

    def of(self, proposal_id):
        return self.find({"proposal_id": proposal_id})
