from .core import Repository
from .config import users


class UsersRepository(Repository):
    """Provides interface for Users collection of database."""

    def __init__(self):
        super().__init__(users)

    def with_permission(self, permission):
        # todo not effective
        from gem.db import roles

        result = []
        for user in self.all():
            role = roles.find_one({"name": user.role})
            if permission in role.permissions:
                result.append(user)
        return result
