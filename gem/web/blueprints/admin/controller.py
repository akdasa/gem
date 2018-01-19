from gem.db import articles
from gem.web.blueprints.crud_controller import CrudController


class AdminController(CrudController):
    def __init__(self):
        super().__init__(articles, namespace="admin", columns=["name"], permission="admin",
                         script=["app/admin.js"])

    def _update_model(self, model, data):
        model.name = data.get("name", None)
        model.value = data.get("value", None)
