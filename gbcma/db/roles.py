from .core import Repository
from .config import roles


class RolesRepository(Repository):
    """Provides interface for Roles collection of database."""

    def __init__(self):
        super().__init__(roles)
