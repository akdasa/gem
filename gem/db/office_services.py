from .core import Repository
from .config import services


class OfficeServicesRepository(Repository):
    """Provides interface for OfficeService collection of database."""

    def __init__(self):
        super().__init__(services)

    def of(self, office_name):
        return self.find({"office": office_name})

    def create(self, office, name):
        self.insert({
            "office": office,
            "name": name
        })
