from gem.db.comments import CommentsRepository
from gem.db.proposals import ProposalsRepository
from gem.db.sessions import SessionsRepository
from gem.db.users import UsersRepository
from gem.db.votes import VotesRepository
from gem.db.roles import RolesRepository
from gem.db.laws import LawsRepository

proposals = ProposalsRepository()
users = UsersRepository()
sessions = SessionsRepository()
votes = VotesRepository()
comments = CommentsRepository()
roles = RolesRepository()
laws = LawsRepository()
