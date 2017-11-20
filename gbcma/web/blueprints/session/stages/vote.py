from gbcma.db import votes, users
from gbcma.web.blueprints.session.stages.stage import SessionStage


class VotingSessionStage(SessionStage):
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
            y = self.__votes_by("yes", v)
            n = self.__votes_by("no", v)
            u = self.__votes_by("undecided", v)

            # let's use count from document if session without
            # any person who can vote
            a = y + n + u if can_vote_count == 0 else max(can_vote_count, y+n+u)
            a = max(a, 1)

            result["votes"]["progress"] = {
                "yes": y,
                "no": n,
                "unknown": u,
                "yes_p": round(y / a * 100, 2),
                "no_p": round(n / a * 100, 2),
                "unknown_p": round(u / a * 100, 2),
                "total": a,
                "voted": y + n + u
            }
            result["votes"]["roles"] = {}

            for user_id in doc["votes"]:
                user = users.get(user_id)
                value = doc["votes"][user_id]
                role = user["role"]
                if role not in result["votes"]["roles"]:
                    result["votes"]["roles"][role] = {"yes": 0,"no": 0,"undecided": 0}
                if value in ["yes", "no", "undecided"]:
                    result["votes"]["roles"][role][value] += 1
                # result["votes"]["a"]

        return result

    @staticmethod
    def __users_can_vote(users):
        can_vote = filter(lambda x: x.has_permission("vote"), users)
        can_vote_count = len(list(can_vote))
        return can_vote_count

    @staticmethod
    def __votes_by(value, ar):
        return len(list(filter(lambda x: ar[x] == value, ar)))