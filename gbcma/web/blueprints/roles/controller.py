from gbcma.web.blueprints.crud_controller import CrudController


class RolesController(CrudController):
    def __init__(self, repository):
        super().__init__(repository, namespace="roles")
        self._columns = ["name"]

    def _form_to_dict(self, form, d):
        d.update({
            "name": form.get("name", None),
            "permissions": list(filter(None, str.split(form.get("permissions", ""), " ")))
        })
        return d
