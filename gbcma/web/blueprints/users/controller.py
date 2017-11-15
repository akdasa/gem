from gbcma.db import roles
from gbcma.web.blueprints.crud_controller import CrudController


class UsersController(CrudController):
    def __init__(self, repository):
        super().__init__(repository, namespace="users")
        self._columns = ["name", "role"]

    def _form_to_dict(self, form, d):
        d.update({
            "name": form.get("name", None),
            "login": form.get("login", None),
            "password": form.get("password", ""),
            "role": form.get("role", None)
        })
        return d

    def _extend(self, model):
        r = list(map(lambda x: x["name"], roles.search({})))
        return {"roles": r}
