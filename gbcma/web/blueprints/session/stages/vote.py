from gbcma.db import votes
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
        voted = len(self.__votes)

        # calculate votes
        t = voted if can_vote_count == 0 else max(can_vote_count, voted)

        # result
        return { "voted": voted, "total": t }

    @staticmethod
    def __users_can_vote(users):
        """Return list of users can vote
        :rtype: list
        :param users:
        :return: List of users can vote"""
        return list(filter(lambda x: x.has_permission("vote"), users))
