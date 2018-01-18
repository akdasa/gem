
class ProposalFlow:
    def __init__(self, proposal):
        """
        Initializes new instance of the ProposalFlow class.
        :type proposal: Proposal
        :param proposal: Proposal
        """
        self.__proposal = proposal

    def start(self):
        state = self.__proposal.state
        if state == "new":
            self.__proposal.state = "deputies_review"

    def move_next(self):
        state = self.__proposal.state
        if state == "new":
            self.__proposal.state = "deputies_review"

        elif state == "deputies_review":
            self.__proposal.state = "straw_vote"

        elif state == "straw_vote":
            self.__proposal.state = "deputies_straw_vote_review"

        elif state == "deputies_straw_vote_review":
            self.__proposal.state = "final_vote"

        elif state == "final_vote":
            self.__proposal.state = "done"

    def get_previous_stage(self):
        if self.__proposal.state in ["new", "deputies_review"]:
            return "new"

        if self.__proposal.state == "straw_vote":
            return "deputies_review"

        if self.__proposal.state == "deputies_straw_vote_review":
            return "straw_vote"

        if self.__proposal.state == "final_vote":
            return "deputies_straw_vote_review"

        if self.__proposal.state == "done":
            return "final_vote"
