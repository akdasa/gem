from gem.db import votes, users


class VotingResultsWidget:
    def __init__(self, proposal_id, stage):
        self.__proposal_id = proposal_id
        self.__stage = stage
        self.__threshold = None
        self.__doc = None
        self.__votes = None
        self.__private = None
        self.__type = None
        self.__threshold = None
        self.update()

    def update(self):
        # todo Do not create
        self.__doc = votes.find_or_create(self.__proposal_id, self.__stage)
        self.__votes = self.__doc.votes
        self.__private = self.__doc.get("private", True)
        self.__type = self.__doc.get("type", None)
        self.__threshold = self.__doc.get("threshold", None)

    def view(self):
        # calculate votes
        y = self.__votes_by("yes")
        n = self.__votes_by("no")
        u = self.__votes_by("undecided")
        z = self.__votes_by("none")
        t = y + n + u + z  # if can_vote_count == 0 else max(can_vote_count, y + n + u)
        th = self.__threshold
        status = \
            "tie" if y == n and th == "majority" else \
            "pass" if y > n and th == "majority" else \
            "pass" if y > t * 0.66 and th == "2/3" else \
            "pass" if y > t * .8 and th == "4/5" else \
            "pass" if y == t and th == "unanimous" else "fail"

        # result
        return {
            "yes": y, "no": n, "undecided": u, "non_vote": z,
            "voted": y + n + u, "total": t,
            "roles": self.__details(),
            "threshold": th, "status": status, "type": self.__type
        }

    def __details(self):
        result = {}
        for row_id in self.__votes:
            value = self.__votes[row_id]
            user_id = value.get("user_id", None)
            user = users.get(user_id) if not self.__private else None
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
                if not self.__doc.private:
                    result[role]["who"][vote].append(user_name)

        return result

    def __votes_by(self, value):
        """Returns count of votes for specific value
        :type value: str
        :rtype: int
        :param value: Vote type
        :return: Count of votes"""
        return len(list(filter(lambda x: self.__votes[x]["vote"] == value, self.__votes)))