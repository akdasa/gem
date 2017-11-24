from gbcma.web.blueprints.crud_controller import CrudController


class ProposalsController(CrudController):
    def __init__(self, repository):
        """Initializes new instance of the ProposalsController class
        :type repository: ProposalsRepository
        :param repository: Repository to manipulate entities in."""
        super().__init__(repository, namespace="proposals", columns=["key", "title"])

    def search(self, term):
        """Returns list of proposals found by title.
        :param term: Query.
        :return: List of documents { key, title }."""
        data = self._repository.search_by_title(term)
        result = map(self.__map, data)
        return list(result)

    def _update_model(self, model, data):
        model.update({
            "key": data.get("key", None),
            "title": data.get("title", None),
            "content": data.get("content", None)
        })

    @staticmethod
    def __map(x):
        return {
            "title": x["title"],
            "key": str(x["_id"])
        }
