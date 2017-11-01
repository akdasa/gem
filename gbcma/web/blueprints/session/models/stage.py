from gbcma.db.users import UsersRepository
from gbcma.db.votes import VotesRepository
from gbcma.event import Event


class SessionStage:
    def __init__(self, session, proposal, position=(0, 0)):
        self.__session = session
        self.__proposal = proposal
        self.__position = position

        self.__voted = Event()
        self.__commented = Event()

    @property
    def voted(self):
        return self.__voted

    @property
    def commented(self):
        return self.__commented

    def vote(self, user, value):
        proposal_id = self.__proposal["_id"]
        votes = VotesRepository()
        doc = votes.find({"proposal_id": proposal_id})
        if not doc:
            doc = votes.create(proposal_id)
        if "votes" not in doc:
            doc["votes"] = {}
        doc["votes"][user.get_id()] = value
        votes.save(doc)
        self.__voted.notify()
        return True

    def comment(self, user, message, quote=None):
        pass

    @property
    def view(self):
        votes = VotesRepository().find({"proposal_id": self.__proposal["_id"]})
        users = UsersRepository()

        result = {
            "proposal": {"title": self.__proposal["title"], "content": self.__proposal["content"]},
            "progress": {"current": self.__position[0] + 1, "total": self.__position[1]}
        }

        if votes:
            result["votes"] = list(
                map(lambda x: {"id": x, "value": votes["votes"][x], "name": users.get(x)["name"]},
                    votes["votes"]))
            result["votes_progress"] = {
                "current": len(result["votes"]),
                "total": len(self.__session.users.all)
            }

        return result
