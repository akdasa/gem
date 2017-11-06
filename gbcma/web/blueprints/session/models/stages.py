from gbcma.db.proposals import ProposalsRepository
from gbcma.db.sessions import SessionsRepository
from gbcma.event import Event
from .stage import SessionStage


class SessionStages:
    def __init__(self, session):
        self.__session = session
        self.__stages = self.__create_stages(session.session_id)
        self.__stage_idx = 0

        self.__changed = Event()

    @property
    def changed(self):
        return self.__changed

    @property
    def current(self):
        return self.__stages[self.__stage_idx]

    def change(self, step=1):
        self.__stage_idx += step
        if self.__stage_idx <= 0:
            self.__stage_idx = 0
        if self.__stage_idx >= len(self.__stages):
            self.__stage_idx = len(self.__stages) - 1

        self.__changed.notify(self.current)
        return True

    def __create_stages(self, session_id):
        stages = []
        session = SessionsRepository().get(session_id)
        proposals = ProposalsRepository().search_list(session["proposals"])
        count = len(proposals)

        for idx, proposal in enumerate(proposals):
            stage = SessionStage(self.__session, proposal, position=(idx, count))

            stage.voted.subscribe(self.__on_stage_changed)
            stage.commented.subscribe(self.__on_stage_changed)

            stages.append(stage)
        return stages

    def __on_stage_changed(self, *options):
        self.__changed.notify(self.current)
