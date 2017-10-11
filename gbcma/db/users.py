from gbcma.db.repository import Repository
from .config import users


class UsersRepository(Repository):
    """Provides interface for Users collection of database."""

    def __init__(self):
        super().__init__(users)
