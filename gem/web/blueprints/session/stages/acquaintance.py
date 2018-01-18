from gem.db import comments, users
from gem.web.app.flow import ProposalFlow
from .stage import SessionStage


class AcquaintanceSessionStage(SessionStage):
    """The stage of acquaintance with the proposal."""
    def __init__(self, session, proposal):
        super().__init__(session, proposal)
        self.__comments = []
        self.__proposal = proposal
        self.__previous_stage = ProposalFlow(proposal).get_previous_stage()

    def on_enter(self):
        self.__comments = list(map(lambda x: self.__map(x),
                                   comments.of(self.__proposal.id, self.__previous_stage)))

    @property
    def view(self):
        return {
            "comments": self.__comments
        }

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