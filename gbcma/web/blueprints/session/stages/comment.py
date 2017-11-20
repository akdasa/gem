from gbcma.db import comments, users
from gbcma.web.blueprints.session.stages.stage import SessionStage


class CommentingSessionStage(SessionStage):
    """Represents one stage of the Session."""
    @property
    def view(self):
        """Returns JSON representation of the stage"""
        docs = comments.search({"proposal_id": self.proposal_id})
        return {
            "comments": list(map(self.__map_comment, docs))
        }

    def comment(self, user, message, kind, quote=None):
        comments.create(self.proposal_id, user.id, message, kind, quote)
        self.changed.notify()
        return True

    @staticmethod
    def __map_comment(x):
        return {
            "content": x["content"],
            "type": x["type"],
            "quote": x["quote"],
            "user": users.get(x["user_id"])["name"]
        }
