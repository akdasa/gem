from flask import jsonify

from gbcma.web.blueprints.crud_controller import CrudController


class SessionsController(CrudController):
    def __init__(self, repository):
        super().__init__(repository, namespace="sessions")
        self._columns = ["title", "status"]

        self.register_action("run", "play")
        self.register_action("stop", "pause")
        self.register_js("sessions_controller.js")

    def _form_to_dict(self, form, d):
        d.update({
            "title": form.get("title", None),
            "agenda": form.get("agenda", None),
            "date": form.get("date", None)
        })
        return d

    def run(self, request, key):
        json = request.get_json(force=True)
        status = json.get("status", None)
        if status:  # todo: check status is valid
            s = self._repository.get(key)
            s["status"] = status
            self._repository.save(s)
            return jsonify({"success": True})
        else:
            return jsonify({"success": False})
