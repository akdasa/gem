import configparser

from flask import flash, redirect, render_template, request
from flask_login import logout_user, login_user

from gem.db import users, sessions
from gem.web.app.auth import User


class LoginController:
    def login(self):
        config = configparser.ConfigParser()
        config.read("config.ini")
        allow_empty_password_login = config.getboolean("users", "allow_empty_password_login", fallback=False)

        if request.method == "POST":
            data = request.form
            lgn = data.get("login", None)
            password = data.get("password", None)

            if not allow_empty_password_login:
                user = users.find_one(
                    {"$and": [{"password": password}, {"$or": [{"login": lgn}, {"name": lgn}]}]})
            else:
                user = users.find_one({"$or": [{"login": lgn}, {"name": lgn}]})

            if user:
                u = User(user)
                login_user(u, remember=True)
                flash("You have successfully logged in", category="success")

                # hotfix for presentation
                session = sessions.find_one({"status": "run"})
                if session:
                    return redirect("/session/" + str(session.get("_id")))

                return redirect("/")
            else:
                flash("User with specified login/password pair not found", category="danger")
                return redirect("/")

    def logout(self):
        logout_user()
        flash("You have successfully logged out", category="success")
        return redirect("/")
