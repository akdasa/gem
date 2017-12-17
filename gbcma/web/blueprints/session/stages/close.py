from .stage import SessionStage


class ClosedSessionStage(SessionStage):
    """Session is closed."""

    def __init__(self, session):
        """Initializes new instance of the ClosedSessionStage class.
        :param session: Session"""
        super().__init__(session, None)
