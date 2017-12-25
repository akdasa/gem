from gem.db import comments, users, roles
from .stage import SessionStage


class CommentingSessionStage(SessionStage):
    """The stage of commenting for the document."""

    def __init__(self, session, proposal):
        super().__init__(session, proposal)
        self.__private = True  # show comments on users' pages

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

    def manage(self, data, user=None):
        self.__private = data.get("private", True)
        self.changed.notify()

    @property
    def view(self):
        docs = comments.of(self.proposal.id)
        return {
            "comments": list(map(self.__map, docs)),
            "private": self.__private,
            "roles": self.__roles_can_comment()}

    @staticmethod
    def __roles_can_comment():
        roles_doc = roles.all()
        commenting_roles = filter(lambda x: "comment" in x.permissions, roles_doc)
        role_names = map(lambda x: x.name, commenting_roles)
        return list(role_names)

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
