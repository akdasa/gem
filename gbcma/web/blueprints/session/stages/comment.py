from gbcma.db import comments, users
from .stage import SessionStage


class CommentingSessionStage(SessionStage):
    """The stage of commenting for the document."""

    def comment(self, user, message, kind, quote=None):
        """Create comment
        :type user: User
        :type message: str
        :type kind: str
        :type quote: str
        :param user: User
        :param message: Message
        :param kind: Kind
        :param quote: Quote
        :return: true on success"""
        comments.create(self.proposal.id, user.id, message, kind, quote)
        self.changed.notify()
        return True

    @property
    def view(self):
        docs = comments.of(self.proposal.id)
        return {"comments": list(map(self.__map, docs))}

    @staticmethod
    def __map(x):
        user = users.get(x.user_id)
        return {
            "content": x.content,
            "type": x.type,
            "quote": x.quote,
            "user": user.name,
            "role": user.role
        }
