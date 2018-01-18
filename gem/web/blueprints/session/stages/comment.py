from gem.db import comments, roles
from .stage import SessionStage
from .widgets import CommentsWidget


class CommentingSessionStage(SessionStage):
    """The stage of commenting for the document."""

    def __init__(self, session, proposal):
        super().__init__(session, proposal)
        self.__private = True  # show comments on users' pages
        self.__stage = proposal.state
        self.__roles_can_comment = []
        self.__widget = CommentsWidget(proposal.id, self.__stage)

    def on_enter(self):
        roles_doc = roles.all()
        commenting_roles = filter(lambda x: "comment" in x.permissions, roles_doc)
        self.__roles_can_comment = list(map(lambda x: x.name, commenting_roles))

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
        comments.create(self.proposal.id, user.id, message, kind, self.__stage, quote)
        self.__widget.update()
        self.changed.notify()
        return True

    def manage(self, data, user=None):
        self.__private = data.get("private", True)
        self.changed.notify()

    @property
    def view(self):
        return {
            "comments": self.__widget.view(),
            "private": self.__private,
            "roles": self.__roles_can_comment
        }

