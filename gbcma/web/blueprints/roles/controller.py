from gbcma.web.blueprints.crud_controller import CrudController


class RolesController(CrudController):
    def __init__(self, repository):
        super().__init__(repository, namespace="roles")
        self._columns = ["name"]

    def _update_model(self, model, data):
        model.update({
            "name": data.get("name", None),
            "permissions": list(filter(None, str.split(data.get("permissions", ""), " ")))
        })
