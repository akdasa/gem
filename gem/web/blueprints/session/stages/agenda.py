from gem.db import sessions
from .stage import SessionStage


class AgendaSessionStage(SessionStage):
    """Agenda stage."""

    def __init__(self, session, stages):
        """Initializes new instance of the AgendaSessionStage class.
        :param session: Session to which the stage belongs
        :param stages: List of stages"""
        super().__init__(session, None)
        self.__stages = stages

    @property
    def view(self):
        # retrieve session document from db
        session_doc = sessions.get(self.session.session_id)

        # get list of proposals keyed by id:
        # { proposal.id: { title: proposal.title } }
        # it will return list on unique proposals used in the stages
        result = {
            stage.proposal.id: {"title": stage.proposal.title}
            for stage in self.__stages_with_proposal()
        }

        # returns view of the stage
        return {
            "agenda": session_doc.agenda,
            "proposals": list(result.values())
        }

    def __stages_with_proposal(self):
        """Returns list of stages with proposals
        :rtype: list
        :return: Stages"""
        return filter(lambda x: x.proposal, self.__stages)
