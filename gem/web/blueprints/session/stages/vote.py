import hashlib

from gem.db import votes, users
from .stage import SessionStage
from .widgets import VotingResultsWidget


class VotingSessionStage(SessionStage):
    """The stage of voting for the document."""

    def __init__(self, session, proposal, final=False):
        """Initializes new instance of the VotingSessionStage class.
        :type session: Session
        :type proposal: Proposal
        :param session: Session to which the stage belongs
        :param proposal: Proposal document"""
        super().__init__(session, proposal)
        self.__doc = None
        self.__votes = None
        self.__private = True
        self.__type = None
        self.__threshold = None
        self.__stage = proposal.state
        self.__final = final

    def on_enter(self):
        self.__doc = votes.find_or_create(self.proposal.id, self.__stage)
        self.__votes = self.__doc.votes
        self.__private = self.__doc.get("private", True)
        self.__type = self.__doc.get("type", None)
        self.__threshold = self.__doc.get("threshold", None)

    def on_leave(self):
        self.__doc.private = self.__private
        if self.__threshold or self.__final:
            self.__doc.threshold = self.__threshold or "majority"
        if self.__private:
            self.__anonymize()
        if self.__final:
            self.__doc.type = "final"
            self.__fill_none()
        votes.save(self.__doc)

    def vote(self, user, value):
        """Commit a vote for the proposal.
        :param user: User
        :param value: Vote value
        :return: True on success"""
        user_id = self.__user_id_hash(user.id)

        prev = self.__votes.get(user_id, None)
        prev_vote = prev["vote"] if prev else None

        self.__votes[user_id] = {"vote": value, "role": user.role}
        self.__votes[user_id]["user_id"] = user.id
        self.changed.notify()
        return {"success": True, "value": value, "prev": prev_vote}

    def manage(self, data, user=None):
        cmd = data.get("cmd", None)

        if cmd == "set_private":
            self.__private = data.get("value", True)
        if cmd == "set_threshold":
            self.__threshold = data.get("value", "majority")
        self.changed.notify()

    @property
    def view(self):
        can_vote_count = len(self._users_can_vote())
        voted = len(self.__votes)
        t = voted if can_vote_count == 0 else max(can_vote_count, voted)
        return {
            "can_vote": can_vote_count,
            "voted": voted,
            "total": t,
            "private": self.__private,
            "type": "straw" if not self.__final else "final",
            "quorum": self.session.quorum.value,
            "threshold": self.__threshold
        }

    def __anonymize(self):
        """Removes any personal information form document"""
        for row_id in self.__votes:
            if "user_id" in self.__votes[row_id]:
                del self.__votes[row_id]["user_id"]

    @staticmethod
    def __user_id_hash(key):
        return hashlib.sha224(str(key).encode("utf-8")).hexdigest()

    def _users_can_vote(self):
        """Return list of users can vote
        :rtype: list
        :return: List of users can vote"""
        all_users = self.session.users.all
        return list(filter(lambda x: x.has_permission("vote"), all_users))

    def __fill_none(self):
        u = self._users_can_vote()
        a = {user.id: self.__votes.get(self.__user_id_hash(user.id), None) for user in u}
        n = list(filter(lambda x: a[x] is None, a))  # filter out users with submitted vote
        for uid in n: # list of user_ids with no submitted vote
            user = users.get(uid)
            self.vote(user, "none")  # vote as undecided


class VotingResultsSessionStage(SessionStage):
    """The stage of voting for the document."""

    def __init__(self, session, proposal):
        """Initializes new instance of the VotingSessionStage class.
        :type session: Session
        :type proposal: Proposal
        :param session: Session to which the stage belongs
        :param proposal: Proposal document"""
        super().__init__(session, proposal)
        self.__widget = VotingResultsWidget(proposal.id, proposal.state)

    def on_enter(self):
        self.__widget.update()

    @property
    def view(self):
        return self.__widget.view()
