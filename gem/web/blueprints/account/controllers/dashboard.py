import itertools

from flask import render_template
from flask_login import login_required, current_user

from gem.db import proposals, sessions


class DashboardController:
    @login_required
    def index(self):
        sessions_list = self.__upcoming_sessions_for_user(current_user)
        proposals_map = self.__get_proposals_of_sessions(sessions_list)

        return render_template("account_dashboard.html", sessions=sessions_list, proposals=proposals_map)

    @staticmethod
    def __upcoming_sessions_for_user(user):
        upcoming = sessions.upcoming()
        result = filter(lambda x: user.role in x["permissions"]["presence"], upcoming)
        return list(result)

    @staticmethod
    def __get_proposals_of_sessions(sessions_list):
        ids = map(lambda x: x.get("proposals"), sessions_list)
        ids = list(itertools.chain(*ids))
        objs = proposals.find({"_id": {"$in": ids}})
        return {key["_id"]: key for key in objs}
