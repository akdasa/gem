from bson import ObjectId

from .core import Repository
from .config import orders


class OfficeOrdersRepository(Repository):
    """Provides interface for OfficeOrder collection of database."""

    def __init__(self):
        super().__init__(orders)

    def of(self, office_name):
        return self.find({"office": office_name})

    def create(self, office, user_id, service_id, message=None):
        self.insert({
            "office": office,
            "user_id": ObjectId(user_id),
            "service_id": ObjectId(service_id),
            "message": message
        })
