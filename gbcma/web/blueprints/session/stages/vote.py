from gbcma.db import votes, users
from gbcma.web.blueprints.session.stages.stage import SessionStage


class VotingSessionStage(SessionStage):
    """The stage of voting for the document."""

    def __init__(self, session, proposal):
        """Initializes new instance of the VotingSessionStage class."""
        super().__init__(session, proposal)
        self.__doc = votes.find_or_create(self.proposal_id)

    def vote(self, user, value):
        """Commit a vote for the proposal.
        :param user: User
        :param value: Vote value
        :return: True on success
        """
        self.__doc["votes"][user.id] = value
        votes.save(self.__doc)
        self.changed.notify()
        return True

    @property
    def view(self):
        """Returns JSON representation of the stage"""
        can_vote_count = len(self.__users_can_vote(self.session.users.all))

        # calculate votes
        v = self.__doc["votes"]
        y = self.__votes_by("yes", v)
        n = self.__votes_by("no", v)
        u = self.__votes_by("undecided", v)

        # let's use count from document if session without any person who can vote
        t = y + n + u if can_vote_count == 0 else max(can_vote_count, y + n + u)

        result = {
            "yes": y, "no": n, "undecided": u,
            "voted": y + n + u, "total": t,
            "roles": {}
        }

        # calculate voted keyed by role
        for user_id in self.__doc["votes"]:
            user = users.get(user_id)
            value = self.__doc["votes"][user_id]
            role = user["role"]
            if role not in result["roles"]:
                result["roles"][role] = {"yes": 0, "no": 0, "undecided": 0}
            if value in ["yes", "no", "undecided"]:
                result["roles"][role][value] += 1

        return result

    @staticmethod
    def __users_can_vote(users):
        can_vote = filter(lambda x: x.has_permission("vote"), users)
        can_vote_count = list(can_vote)
        return can_vote_count

    @staticmethod
    def __votes_by(value, ar):
        return len(list(filter(lambda x: ar[x] == value, ar)))
