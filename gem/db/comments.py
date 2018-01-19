import datetime

from bson import ObjectId

from .config import comments
from .core import Repository


class CommentsRepository(Repository):
    """Provides interface for Comments collection of database."""

    def __init__(self):
        super().__init__(comments)

    def create(self, proposal_id, user_id, content, kind, stage, quote=None):
        today = datetime.datetime.now()
        inserted_id = self._collection.insert_one({
            "proposal_id": ObjectId(proposal_id),
            "user_id": ObjectId(user_id),
            "content": content,
            "type": kind,
            "quote": quote,
            "stage": stage,
            "timestamp": today.isoformat()
        }).inserted_id
        return self.get(inserted_id)

    def of(self, proposal_id, stage):
        result = self.find({"proposal_id": proposal_id, "stage": stage})
        return sorted(result, key=lambda x: x.get("timestamp", ""))
