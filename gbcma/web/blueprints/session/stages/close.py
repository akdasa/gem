from .stage import SessionStage


class ClosedSessionStage(SessionStage):
    def __init__(self, session):
        super().__init__(session, None)
