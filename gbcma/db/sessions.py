from gbcma.db.repository import Repository
from .config import sessions


class SessionsRepository(Repository):
    """Provides interface for Users collection of database."""

    def __init__(self):
        super().__init__(sessions)
