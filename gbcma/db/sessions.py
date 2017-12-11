import datetime

from .core import Repository
from .config import sessions


class SessionsRepository(Repository):
    """Provides interface for Users collection of database."""

    def __init__(self):
        super().__init__(sessions)

    def active(self):
        return self._collection.find({"status": "run"})

    def upcoming(self):
        now = datetime.datetime.now()

        return self._collection.find({
            "date": {
                "$gte": now.isoformat()
            }
        })
