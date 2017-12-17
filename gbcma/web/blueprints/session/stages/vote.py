from gbcma.db import votes, users
from .stage import SessionStage


class VotingSessionStage(SessionStage):
    """The stage of voting for the document."""

    def __init__(self, session, proposal):
        """Initializes new instance of the VotingSessionStage class.
        :type session: Session
        :type proposal: Proposal
        :param session: Session to which the stage belongs
        :param proposal: Proposal document"""
        super().__init__(session, proposal)
        self.__doc = votes.find_or_create(self.proposal.id)
        self.__votes = self.__doc.votes

    def vote(self, user, value):
        """Commit a vote for the proposal.
        :param user: User
        :param value: Vote value
        :return: True on success"""
        self.__votes[user.id] = value
        votes.save(self.__doc)
        self.changed.notify()
        return True

    @property
    def view(self):
        all_users = self.session.users.all
        can_vote_count = len(self.__users_can_vote(all_users))

        # calculate votes
        y = self.__votes_by("yes")
        n = self.__votes_by("no")
        u = self.__votes_by("undecided")
        t = y + n + u if can_vote_count == 0 else max(can_vote_count, y + n + u)

        # calculate votes keyed by role
        roles = {}
        for user_id in self.__votes:
            user = users.get(user_id)
            role = user.role
            value = self.__votes[user_id]

            # add empty data for new role
            if role not in roles:
                roles[role] = {
                    "yes": 0, "no": 0, "undecided": 0,
                    "who": {"yes": [], "no": [], "undecided": []}
                }

            # count vote and append person into "who" section
            if value in ["yes", "no", "undecided"]:
                roles[role][value] += 1
                roles[role]["who"][value].append(user.name)

        # result
        return {
            "yes": y, "no": n, "undecided": u,
            "voted": y + n + u, "total": t,
            "roles": roles
        }

    @staticmethod
    def __users_can_vote(users):
        """Return list of users can vote
        :rtype: list
        :param users:
        :return: List of users can vote"""
        return list(filter(lambda x: x.has_permission("vote"), users))

    def __votes_by(self, value):
        """Returns count of votes for specific value
        :type value: str
        :rtype: int
        :param value: Vote type
        :return: Count of votes"""
        return len(list(filter(lambda x: self.__votes[x] == value, self.__votes)))
