from gbcma.db import sessions
from .stage import SessionStage


class AgendaSessionStage(SessionStage):
    """The stage of acquaintance with the proposal."""
    def __init__(self, session, stages):
        super().__init__(session, None)
        self.__stages = stages
        self.__doc = sessions.get(self.session.session_id)
        self.__agenda = self.__doc["agenda"] if self.__doc else None

    @property
    def view(self):
        result = []
        last_proposal_id = None
        stages_with_proposal = \
            filter(lambda x: x.proposal, self.__stages)

        for stage in stages_with_proposal:
            if last_proposal_id != stage.proposal_id:
                last_proposal_id = stage.proposal_id
                result.append({
                    "title": stage.proposal["title"],
                    "stages": []
                })
            else:
                last_idx = len(result) - 1
                result[last_idx]["stages"].append(stage.kind)

        return {
            "agenda": self.__agenda,
            "proposals": result
        }
