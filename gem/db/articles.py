from gem.db.config import articles
from .core import Repository


class ArticlesRepository(Repository):
    """Provides interface for Articles collection of database."""

    def __init__(self):
        super().__init__(articles)
