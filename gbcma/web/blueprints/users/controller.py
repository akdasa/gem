from gbcma.db import roles
from gbcma.web.blueprints.crud_controller import CrudController


class UsersController(CrudController):
    def __init__(self, repository):
        super().__init__(repository, namespace="users")
        self._columns = ["name", "role"]

    def _update_model(self, model, data):
        model.update({
            "name": data.get("name", None),
            "login": data.get("login", None),
            "password": data.get("password", ""),
            "role": data.get("role", None)
        })

    def _extend(self, model):
        r = list(map(lambda x: x["name"], roles.search({})))
        return {"roles": r}
