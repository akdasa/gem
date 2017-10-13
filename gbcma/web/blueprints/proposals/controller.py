from gbcma.web.blueprints.crud_controller import CrudController


class ProposalsController(CrudController):
    def __init__(self, repository):
        super().__init__(repository, namespace="proposals")
        self._columns = ["title"]

    def _form_to_dict(self, form, d):
        d.update({
            "title": form.get("title", None),
            "content": form.get("content", None)
        })
        return d
