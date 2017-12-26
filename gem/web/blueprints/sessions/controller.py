from bson import ObjectId
from flask import jsonify
from flask_login import login_required

from gem.db import roles, proposals, sessions
from gem.web.blueprints.crud_controller import CrudController


class SessionsController(CrudController):
    def __init__(self):
        super().__init__(sessions, namespace="sessions", columns=["title", "date", "status"],
                         row_class=self.__row_class)

        self.add_action("run", "play")
        self.add_action("stop", "pause")
        self.add_action("manage", "hand-right", "session.manage")
        self.add_script("app/sessions.js")

    @login_required
    def run(self, request, key):
        json = request.get_json(force=True)
        status = json.get("status", None)
        if status:  # todo: check status is valid
            s = self._repository.get(key)
            s.status = status
            self._repository.save(s)
            return jsonify({"success": True})
        else:
            return jsonify({"success": False})

    def _update_model(self, model, data):
        ids_list = filter(None, data.get("proposals", "").split(","))
        ids = list(map(lambda x: ObjectId(x), ids_list))

        presence = data.getlist("presence")
        vote = data.getlist("vote")

        model.title = data.get("title", None)
        model.agenda = data.get("agenda", None)
        model.date = data.get("date", None)
        model.proposals = ids
        model.permissions = {
            "presence": presence,
            "vote": vote
        }

    def _extend(self, model):
        result_proposals = {}

        if model:
            d = proposals.find({"_id": {"$in": model.get("proposals", [])}})
            result_proposals = {str(key["_id"]): without_keys(key, ["_id"]) for key in d}

        role_docs = roles.all()
        result_roles = map(lambda x: x["name"], role_docs)

        return {"proposals_objects": result_proposals, "roles": list(result_roles)}

    @staticmethod
    def __row_class(model):
        status = model.get("status", None)
        return \
            "success" if status == "closed" else \
            "warning" if status == "run" else ""

def without_keys(d, keys):
    return {x: d[x] for x in d if x not in keys}
