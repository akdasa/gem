from gbcma.event import Event


class SessionStage:
    def __init__(self, session, proposal):
        """
        Initializes new instance of the SessionStage class.
        :param session: Session
        :param proposal: Proposal document
        """
        self.__session = session
        self.__proposal = proposal
        self.__changed = Event()

    @property
    def kind(self):
        return self.__kind(self.__class__.__name__)

    @property
    def changed(self):
        return self.__changed

    @property
    def proposal(self):
        return self.__proposal

    @property
    def proposal_id(self):
        return self.__proposal["_id"]

    @property
    def session(self):
        return self.__session

    @property
    def view(self):
        return {}

    @staticmethod
    def __kind(name):
        if len(name) > 12:
            return name.replace("SessionStage", "").lower()
        else:
            return name
