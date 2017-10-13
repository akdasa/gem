from gbcma.web.blueprints.crud_controller import CrudController


class SessionsController(CrudController):
    def __init__(self, repository):
        super().__init__(repository, namespace="sessions")
        self._columns = ["title"]

    def _form_to_dict(self, form, d):
        d.update({
            "title": form.get("title", None),
            "agenda": form.get("agenda", None)
        })
        return d
