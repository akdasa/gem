from gbcma.db import comments, users
from gbcma.web.blueprints.session.stages.stage import SessionStage


class CommentingSessionStage(SessionStage):
    """The stage of commenting for the document."""

    @property
    def view(self):
        """Returns JSON representation of the stage"""
        docs = comments.of(self.proposal_id)
        return {"comments": list(map(self.__map, docs))}

    def comment(self, user, message, kind, quote=None):
        comments.create(self.proposal_id, user.id, message, kind, quote)
        self.changed.notify()
        return True

    @staticmethod
    def __map(x):
        user = users.get(x["user_id"])
        return {
            "content": x["content"],
            "type": x["type"],
            "quote": x["quote"],
            "user": user["name"],
            "role": user["role"]
        }
