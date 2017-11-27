from gbcma.db import roles
from gbcma.web.blueprints.crud_controller import CrudController


class UsersController(CrudController):
    def __init__(self, repository):
        super().__init__(repository, namespace="users",
                         columns=["name", "role"], row_class=self.__row_class)

    @staticmethod
    def __row_class(model):
        print("! ", model)
        return "danger" if model.get("suspend", {}).get("value", False) is True else None

    def _update_model(self, model, data):
        print(data)
        model.update({
            "name": data.get("name", None),
            "login": data.get("login", None),
            "password": data.get("password", ""),
            "role": data.get("role", None),
            "suspend": {
                "value": True if data.get("suspend", False) else False,
                "reason": data.get("suspend-reason", None)
            }
        })

    def _extend(self, model):
        role_docs = roles.search({})
        r = map(lambda x: x["name"], role_docs)
        return {"roles": list(r)}
