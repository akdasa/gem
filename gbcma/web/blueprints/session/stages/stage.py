from gbcma.event import Event


class SessionStage:
    """Represents stage of a Session."""

    def __init__(self, session, proposal):
        """Initializes new instance of the SessionStage class.
        :type session: Session
        :type proposal: Proposal
        :param session: Session to which the stage belongs
        :param proposal: Proposal document"""
        self.__session = session
        self.__proposal = proposal
        self.__changed = Event()

    @property
    def session(self):
        """Returns session stage belongs to
        :rtype: Session
        :return: Session"""
        return self.__session

    @property
    def name(self):
        """Returns name of the stage.
        :rtype: str
        :return: Name"""
        return self.__name(self.__class__.__name__)

    @property
    def changed(self):
        """Stage changed event
        :rtype: Event
        :return: Event"""
        return self.__changed

    @property
    def proposal(self):
        """Returns proposal
        :rtype: Proposal
        :return: Proposal"""
        return self.__proposal

    @property
    def view(self):
        """Returns view presentation of stage
        :rtype: dict
        :return: Dictionary"""
        return {}

    def on_enter(self):
        pass

    def on_leave(self):
        pass

    @staticmethod
    def __name(name):
        return name.replace("SessionStage", "").lower()