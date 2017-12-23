from gem.db import laws
from gem.web.blueprints.crud_controller import CrudController


class LawsController(CrudController):
    def __init__(self):
        """Initializes new instance of the ProposalsController class"""
        print(laws)
        super().__init__(laws, namespace="laws", columns=["key", "title"])

    def _update_model(self, model, data):
        model.key = data.get("key", None)
        model.title = data.get("title", None)
        model.content = data.get("content", None)

    @staticmethod
    def __search_view(x):
        return {
            "title": x.title,
            "key": str(x["_id"])
        }
