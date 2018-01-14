import hashlib
from abc import ABCMeta

from gem.db import votes, users
from .stage import SessionStage


class VotingBaseSessionStage(SessionStage, metaclass=ABCMeta):
    def __init__(self, session, proposal):
        super().__init__(session, proposal)
        self._doc = None
        self._votes = None
        self._private = True
        self._threshold = "majority"

    def on_enter(self):
        self._doc = votes.find_or_create(self.proposal.id)
        self._votes = self._doc.votes
        self._private = self._doc.get("private", True)
        self._threshold = self._doc.get("threshold", "majority")

    def _users_can_vote(self):
        """Return list of users can vote
        :rtype: list
        :return: List of users can vote"""
        all_users = self.session.users.all
        return list(filter(lambda x: x.has_permission("vote"), all_users))

    def _votes_by(self, value):
        """Returns count of votes for specific value
        :type value: str
        :rtype: int
        :param value: Vote type
        :return: Count of votes"""
        return len(list(filter(lambda x: self._votes[x]["vote"] == value, self._votes)))



class VotingSessionStage(VotingBaseSessionStage):
    """The stage of voting for the document."""

    def __init__(self, session, proposal, final=False):
        """Initializes new instance of the VotingSessionStage class.
        :type session: Session
        :type proposal: Proposal
        :param session: Session to which the stage belongs
        :param proposal: Proposal document"""
        super().__init__(session, proposal)
        self.__final = final

    def on_leave(self):
        self._doc.private = self._private
        self._doc.threshold = self._threshold
        if self._private:
            self.__anonymize()
        self.__fill_abstention()
        votes.save(self._doc)

    def vote(self, user, value):
        """Commit a vote for the proposal.
        :param user: User
        :param value: Vote value
        :return: True on success"""
        user_id = self.__user_id_hash(user.id)

        prev = self._votes.get(user_id, None)
        prev_vote = prev["vote"] if prev else None

        self._votes[user_id] = {"vote": value, "role": user.role}
        self._votes[user_id]["user_id"] = user.id
        self.changed.notify()
        return {"success": True, "value": value, "prev": prev_vote}

    def manage(self, data, user=None):
        cmd = data.get("cmd", None)

        if cmd == "set_private":
            self._private = data.get("value", True)
        if cmd == "set_threshold":
            self._threshold = data.get("value", "majority")
        self.changed.notify()

    @property
    def view(self):
        can_vote_count = len(self._users_can_vote())
        voted = len(self._votes)
        t = voted if can_vote_count == 0 else max(can_vote_count, voted)
        return {
            "can_vote": can_vote_count,
            "voted": voted,
            "total": t,
            "private": self._private,
            "type": "straw" if not self.__final else "final",
            "quorum": self.session.quorum.value,
            "threshold": self._threshold
        }

    def __anonymize(self):
        """Removes any personal information form document"""
        for row_id in self._votes:
            if "user_id" in self._votes[row_id]:
                del self._votes[row_id]["user_id"]

    @staticmethod
    def __user_id_hash(key):
        return hashlib.sha224(str(key).encode("utf-8")).hexdigest()

    def __fill_abstention(self):
        u = self._users_can_vote()
        a = {user.id: self._votes.get(self.__user_id_hash(user.id), None) for user in u}
        n = list(filter(lambda x: a[x] is None, a))  # filter out users with submitted vote
        for uid in n: # list of user_ids with no submitted vote
            user = users.get(uid)
            self.vote(user, "undecided")  # vote as undecided

class VotingResultsSessionStage(VotingBaseSessionStage):
    """The stage of voting for the document."""

    def __init__(self, session, proposal):
        """Initializes new instance of the VotingSessionStage class.
        :type session: Session
        :type proposal: Proposal
        :param session: Session to which the stage belongs
        :param proposal: Proposal document"""
        super().__init__(session, proposal)

    @property
    def view(self):
        can_vote_count = len(self._users_can_vote())

        # calculate votes
        y = self._votes_by("yes")
        n = self._votes_by("no")
        u = self._votes_by("undecided")
        t = y + n + u # if can_vote_count == 0 else max(can_vote_count, y + n + u)
        th = self._doc.threshold
        passes = \
            y > n if th == "majority" else \
            y > t * 0.66 if th == "2/3" else \
            y > t * .8 if th == "4/5" else \
            y == t if th == "unanimous" else False

        # result
        return {
            "yes": y, "no": n, "undecided": u,
            "voted": y + n + u, "total": t,
            "roles": self.__details(),
            "threshold": th, "passes": passes
        }

    def __details(self):
        result = {}
        for row_id in self._votes:
            value = self._votes[row_id]
            user_id = value.get("user_id", None)
            user = users.get(user_id) if not self._private else None
            vote = value["vote"]
            user_name = user.name if user else value.get("name", None)
            role = user.role if user else value.get("role", None)

            # add empty data for new role
            if role not in result:
                result[role] = {
                    "yes": 0, "no": 0, "undecided": 0,
                    "who": {"yes": [], "no": [], "undecided": []}
                }

            # count vote and append person into "who" section
            if vote in ["yes", "no", "undecided"]:
                result[role][vote] += 1
                if not self._doc.private:
                    result[role]["who"][vote].append(user_name)

        return result
