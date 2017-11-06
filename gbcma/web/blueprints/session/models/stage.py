from gbcma.db import votes, comments, users
from gbcma.event import Event


class SessionStage:
    """Represents one stage of the Session."""

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

        # events
        self.__voted = Event()
        self.__commented = Event()

    # Events -----------------------------------------------------------------------------------------------------------

    @property
    def voted(self):
        """Raises then user votes."""
        return self.__voted

    @property
    def commented(self):
        """Raises then user add a comment."""
        return self.__commented

    # Properties -------------------------------------------------------------------------------------------------------

    @property
    def votes(self):
        return votes.find({"proposal_id": self.proposal_id})

    @property
    def comments(self):
        return comments.search({"proposal_id": self.proposal_id})

    @property
    def proposal_id(self):
        return self.__proposal["_id"]

    @property
    def view(self):
        """Returns JSON representation of the stage"""
        all_users = self.__session.users.all
        can_vote = filter(lambda x: x.has_permission("vote"), all_users)
        can_vote_count = len(list(can_vote))
        comments = map(_map_comment, self.comments)

        result = {
            "proposal": {"title": self.__proposal["title"], "content": self.__proposal["content"]},
            "comments": list(comments),
            "progress": {"current": self.__position[0] + 1, "total": self.__position[1]},
            "votes_progress": {"total": can_vote_count, "voted": 0}
        }

        if self.votes and can_vote_count > 0:
            v = self.votes["votes"]
            y = _votes_by(True, v)
            n = _votes_by(False, v)
            u = _votes_by(None, v)

            result["votes_progress"] = {
                "yes": y / can_vote_count * 100,
                "no": n / can_vote_count * 100,
                "unknown": u / can_vote_count * 100,
                "total": can_vote_count,
                "voted": y+n+u
            }

        return result

    # Actions ----------------------------------------------------------------------------------------------------------

    def vote(self, user, value):
        doc = votes.find_or_create(self.proposal_id)
        doc["votes"][user.id] = value
        votes.save(doc)
        self.__voted.notify()
        return True

    def comment(self, user, message, kind, quote=None):
        comment = comments.create(self.proposal_id, user.id, message, kind, quote)
        self.commented.notify(comment)
        return True


def _votes_by(value, ar):
    return len(list(filter(lambda x: ar[x] is value, ar)))


def _map_comment(x):
    return {
        "content": x["content"],
        "type": x["type"],
        "quote": x["quote"],
        "user": users.get(x["user_id"])["name"]
    }
