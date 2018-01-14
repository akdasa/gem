from gem.db import proposals
from gem.web.blueprints.crud_controller import CrudController


class ProposalsController(CrudController):
    def __init__(self):
        """Initializes new instance of the ProposalsController class"""
        super().__init__(proposals,
                         namespace="proposals",
                         columns=["key", "title", "state"],
                         script=["app/proposals.js"])

    def search(self, request):
        """Returns list of proposals found by title.
        :param request: Query.
        :return: List of documents { key, title }."""
        term = request.args.get("term", None)
        docs = self._repository.search_by_title(term)
        return list(map(self.__search_view, docs))

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
