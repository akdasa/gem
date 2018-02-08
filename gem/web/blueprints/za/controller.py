from gem.db import za
from gem.web.blueprints.crud_controller import CrudController


class ZaController(CrudController):
    def __init__(self):
        super().__init__(za, namespace="za", columns=["zone", "user"])

    def _update_model(self, model, data):
        model.zone = data.get("zone", None)
        model.user = data.get("user", None)
