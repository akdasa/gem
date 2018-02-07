from gem.db.articles import ArticlesRepository
from gem.db.comments import CommentsRepository
from gem.db.office_services import OfficeServicesRepository
from gem.db.proposals import ProposalsRepository
from gem.db.sessions import SessionsRepository
from gem.db.users import UsersRepository
from gem.db.votes import VotesRepository
from gem.db.roles import RolesRepository
from gem.db.laws import LawsRepository
from gem.db.office_orders import OfficeOrdersRepository

proposals = ProposalsRepository()
users = UsersRepository()
sessions = SessionsRepository()
votes = VotesRepository()
comments = CommentsRepository()
roles = RolesRepository()
laws = LawsRepository()
articles = ArticlesRepository()
orders = OfficeOrdersRepository()
services = OfficeServicesRepository()
