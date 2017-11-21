from gbcma.db import sessions, proposals
from gbcma.event import Event

from gbcma.web.blueprints.session.stages.acquaintance import AcquaintanceSessionStage
from gbcma.web.blueprints.session.stages.close import ClosedSessionStage
from gbcma.web.blueprints.session.stages.comment import CommentingSessionStage
from gbcma.web.blueprints.session.stages.vote import VotingSessionStage
from gbcma.web.blueprints.session.stages.discussion import DiscussionSessionStage


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
    def index(self):
        return self.__stage_idx

    @property
    def count(self):
        return len(self.__stages)

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
        result = []
        session = sessions.get(session_id)  # gets session document
        docs = proposals.search_list(session["proposals"])

        for idx, proposal in enumerate(docs):
            stages = [
                AcquaintanceSessionStage(self.__session, proposal),
                VotingSessionStage(self.__session, proposal),
                CommentingSessionStage(self.__session, proposal),
                DiscussionSessionStage(self.__session, proposal)]

            for stage in stages:
                stage.changed.subscribe(self.__on_stage_changed)
                result.append(stage)

        result.append(ClosedSessionStage(self.__session))
        return result

    def __on_stage_changed(self, *options):
        self.__changed.notify(self.current)
