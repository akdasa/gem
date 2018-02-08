from gem.db.za import za
from gem.db import roles, users
from gem.web.blueprints.crud_controller import CrudController

class ZaController(CrudController):
    def __init__(self):
        super().__init__(za, namespace="za", columns=["name", "role"], row_class=self.__row_class)
        #super().__init__(za, namespace="za", columns=["zone", "user"], row_class=self.__row_class)

    def _update_model(self, model, data):
        model.name = data.get("name", None)
        model.login = data.get("login", None)
        model.password = data.get("password", "")
        model.role = data.get("role", None)
        model.suspend = {
            "value": True if data.get("suspend", False) else False,
            "reason": data.get("suspend-reason", None)
        }

    def _extend(self, model):
        role_docs = roles.all()
        role_view = list(map(lambda x: x.name, role_docs))
        return {"roles": role_view}

    @staticmethod
    def __row_class(model):
        is_suspended = model.get("suspend", {}).get("value", False) is True
        return "danger" if is_suspended else None
