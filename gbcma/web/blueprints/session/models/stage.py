from gbcma.db import votes, comments, users
from gbcma.event import Event


class SessionStage:
    def __init__(self, session, proposal, position=(0, 0)):
        """
        Initializes new instance of the SessionStage class.
        :param session: Session
        :param proposal: Proposal document
        :param position: Position. Tuple (index, all)
        """
        self.__session = session
        self.__proposal = proposal
        self.__position = position
        self.__changed = Event()

    @property
    def kind(self):
        return self.__class__.__name__.\
            replace("SessionStage", "").\
            lower()

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
    def position(self):
        return self.__position


class AcquaintanceSessionStage(SessionStage):
    def __init__(self, session, proposal, position=(0, 0)):
        super().__init__(session, proposal, position)

    @property
    def view(self):
        return {}


class VotingSessionStage(SessionStage):
    def __init__(self, session, proposal, position=(0, 0)):
        super().__init__(session, proposal, position)

    def vote(self, user, value):
        doc = votes.find_or_create(self.proposal_id)
        doc["votes"][user.id] = value
        votes.save(doc)
        self.changed.notify()
        return True

    @property
    def view(self):
        """Returns JSON representation of the stage"""
        doc = votes.find({"proposal_id": self.proposal_id})
        can_vote_count = self.__users_can_vote(self.session.users.all)

        result = {
            "votes": {"progress": {"total": can_vote_count, "voted": 0}}
        }

        if doc:  # if votes document exist
            v = doc["votes"]
            y = self.__votes_by(True, v)
            n = self.__votes_by(False, v)
            u = self.__votes_by(None, v)

            # let's use count from document if session without
            # any person who can vote
            a = y + n + u if can_vote_count == 0 else can_vote_count

            result["votes"]["progress"] = {
                "yes": y / a * 100,
                "no": n / a * 100,
                "unknown": u / a * 100,
                "total": a,
                "voted": y + n + u
            }

        return result

    @staticmethod
    def __users_can_vote(users):
        can_vote = filter(lambda x: x.has_permission("vote"), users)
        can_vote_count = len(list(can_vote))
        return can_vote_count

    @staticmethod
    def __votes_by(value, ar):
        return len(list(filter(lambda x: ar[x] is value, ar)))


class CommentingSessionStage(SessionStage):
    """Represents one stage of the Session."""

    def __init__(self, session, proposal, position=(0, 0)):
        super().__init__(session, proposal, position)

    @property
    def view(self):
        """Returns JSON representation of the stage"""
        docs = comments.search({"proposal_id": self.proposal_id})
        return {
            "comments": list(map(self.__map_comment, docs))
        }

    def comment(self, user, message, kind, quote=None):
        comments.create(self.proposal_id, user.id, message, kind, quote)
        self.changed.notify()
        return True

    @staticmethod
    def __map_comment(x):
        return {
            "content": x["content"],
            "type": x["type"],
            "quote": x["quote"],
            "user": users.get(x["user_id"])["name"]
        }


class ClosedSessionStage(SessionStage):
    def __init__(self, session):
        super().__init__(session, None, None)

    @property
    def view(self):
        return {}
