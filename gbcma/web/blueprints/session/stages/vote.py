from abc import ABCMeta
from gbcma.db import votes, users
from .stage import SessionStage


class VotingBaseSessionStage(SessionStage, metaclass=ABCMeta):
    def __init__(self, session, proposal):
        super().__init__(session, proposal)
        self._doc = None
        self._votes = None

    def on_enter(self):
        self._doc = votes.find_or_create(self.proposal.id)
        self._votes = self._doc.votes

    def on_leave(self):
        votes.save(self._doc)

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
        return len(list(filter(lambda x: self._votes[x] == value, self._votes)))


class VotingSessionStage(VotingBaseSessionStage):
    """The stage of voting for the document."""

    def __init__(self, session, proposal):
        """Initializes new instance of the VotingSessionStage class.
        :type session: Session
        :type proposal: Proposal
        :param session: Session to which the stage belongs
        :param proposal: Proposal document"""
        super().__init__(session, proposal)

    def vote(self, user, value):
        """Commit a vote for the proposal.
        :param user: User
        :param value: Vote value
        :return: True on success"""
        self._votes[user.id] = value
        self.changed.notify()
        return True

    def manage(self, data):
        self._doc.private = data.get("private", True)

    @property
    def view(self):
        can_vote_count = len(self._users_can_vote())
        voted = len(self._votes)
        t = voted if can_vote_count == 0 else max(can_vote_count, voted)
        return {"voted": voted, "total": t, "private": self._doc.private}


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
        t = y + n + u if can_vote_count == 0 else max(can_vote_count, y + n + u)

        # result
        return {
            "yes": y, "no": n, "undecided": u,
            "voted": y + n + u, "total": t,
            "roles": self.__details()
        }

    def __details(self):
        result = {}
        for user_id in self._votes:
            user = users.get(user_id)
            role = user.role
            value = self._votes[user_id]

            # add empty data for new role
            if role not in result:
                result[role] = {
                    "yes": 0, "no": 0, "undecided": 0,
                    "who": {"yes": [], "no": [], "undecided": []}
                }

            # count vote and append person into "who" section
            if value in ["yes", "no", "undecided"]:
                result[role][value] += 1
                if not self._doc.private:
                    result[role]["who"][value].append(user.name)

        return result
