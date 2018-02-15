from gem.db import roles
from gem.web.blueprints.crud_controller import CrudController


class RolesController(CrudController):
    def __init__(self):
        super().__init__(roles, namespace="roles", columns=["name"])
        self._permissions = [
            {"name": "proposals.create", "desc": "Create new proposal"},
            {"name": "proposals.read", "desc": "Read proposal"},
            {"name": "proposals.update", "desc": "Update existing proposal"},
            {"name": "proposals.delete", "desc": "Delete proposal"},
            {"name": "users.create", "desc": "Create new user"},  # 4
            {"name": "users.read", "desc": "Read user data"},
            {"name": "users.update", "desc": "Update existing user"},
            {"name": "users.delete", "desc": "Delete user"},
            {"name": "sessions.create", "desc": "Create new session"},  # 8
            {"name": "sessions.read", "desc": "Read session"},
            {"name": "sessions.update", "desc": "Update existing session"},
            {"name": "sessions.delete", "desc": "Delete session"},
            {"name": "session.manage", "desc": "Manage session"},
            {"name": "session.join", "desc": "Join to session"},
            {"name": "roles.create", "desc": "Create new role"},  # 14
            {"name": "roles.read", "desc": "Read role data"},
            {"name": "roles.update", "desc": "Update existing role"},
            {"name": "roles.delete", "desc": "Delete role"},
            {"name": "laws.create", "desc": "Create new law"},  # 18
            {"name": "laws.read", "desc": "Read law"},
            {"name": "laws.update", "desc": "Update existing law"},
            {"name": "laws.delete", "desc": "Delete law"},
            {"name": "vote", "desc": "Vote"},  # 22
            {"name": "vote.manage", "desc": "Manage"},
            {"name": "comment", "desc": "Comment"},
            {"name": "comment.manage", "desc": "Manage"},
            {"name": "discussion", "desc": "Participate in the discussion"},
            {"name": "discussion.manage", "desc": "Manage discussion: give/withdraw a voice."},
            {"name": "quorum.request_change", "desc": "Request quorum change"},
            {"name": "quorum.change", "desc": "Change quorum value"},
            {"name": "za.create", "desc": "Create new za"},  # 31
            {"name": "za.read", "desc": "Read za"},
            {"name": "za.update", "desc": "Update existing za"},
            {"name": "za.delete", "desc": "Delete za"},
            {"name": "presenter", "desc": "Presenter"},
            {"name": "admin", "desc": "Admin"}]

    def _update_model(self, model, data):
        pl = map(lambda x: x["name"], self._permissions)
        pl = list(filter(lambda x: data.get(x, False), pl))

        model.name = data.get("name", None)
        model.permissions = pl

    def _extend(self, model):
        return {
            "role_groups": [
                {"name": "Proposals", "roles": self._permissions[0:4]},
                {"name": "Users", "roles": self._permissions[4:8]},
                {"name": "Sessions", "roles": self._permissions[8:14]},
                {"name": "Roles", "roles": self._permissions[14:18]},
                {"name": "Laws", "roles": self._permissions[18:22]},
                {"name": "Vote", "roles": self._permissions[22:24]},
                {"name": "Comment", "roles": self._permissions[24:26]},
                {"name": "Discussion", "roles": self._permissions[26:28]},
                {"name": "Misc", "roles": self._permissions[28:30]},
                {"name": "ZA", "roles": self._permissions[30:34]},
                {"name": "Misc", "roles": self._permissions[34:36]}
            ]
        }
