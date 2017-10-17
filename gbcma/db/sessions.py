import datetime

from gbcma.db.repository import Repository
from .config import sessions


class SessionsRepository(Repository):
    """Provides interface for Users collection of database."""

    def __init__(self):
        super().__init__(sessions)

    def active(self):
        return self._c.find({"status": "run"})

    def upcoming(self):
        now = datetime.datetime.now()

        return self._c.find({
            "date": {
                "$gte": now.isoformat()
            }
        })
