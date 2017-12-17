from .stage import SessionStage


class AgendaSessionStage(SessionStage):
    """The stage of acquaintance with the proposal."""

    def __init__(self, session, stages):
        """Initializes new instance of the AgendaSessionStage class.
        :param session: Session to which the stage belongs
        :param stages: List of stages"""
        super().__init__(session, None)
        self.__stages = stages

    @property
    def view(self):
        result = {
            stage.proposal.id: {
                "title": stage.proposal.title,
                "stages": [x.name for x in self.__stages_of_proposal(stage.proposal)]
            } for stage in self.__stages_with_proposal()
        }

        return {
            "agenda": self.session.agenda,
            "proposals": list(result.values())
        }

    def __stages_with_proposal(self):
        """Returns list of stages with proposals
        :rtype: list
        :return: Stages"""
        return filter(lambda x: x.proposal, self.__stages)

    def __stages_of_proposal(self, proposal):
        """Returns list of stages for specified proposal
        :param proposal: Proposal
        :return: List of stages"""
        if not proposal:
            return []
        return filter(lambda x: x.proposal.id == proposal.id, self.__stages_with_proposal())
