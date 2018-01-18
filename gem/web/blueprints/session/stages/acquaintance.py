from gem.web.app.flow import ProposalFlow
from .stage import SessionStage
from .widgets import CommentsWidget


class AcquaintanceSessionStage(SessionStage):
    """The stage of acquaintance with the proposal."""
    def __init__(self, session, proposal):
        super().__init__(session, proposal)
        previous_stage = ProposalFlow(proposal).get_previous_stage()
        self.__comments = CommentsWidget(proposal.id, previous_stage)

    def on_enter(self):
        self.__comments.update()

    @property
    def view(self):
        return {
            "comments": self.__comments.view()
        }
