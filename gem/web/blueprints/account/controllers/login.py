from flask import flash, redirect, render_template, request
from flask_login import logout_user, login_user

from gem.db import users
from gem.web.app.auth import User


class LoginController:
    def login(self):
        if request.method == "POST":
            data = request.form
            lgn = data.get("login", None)
            password = data.get("password", None)

            user = users.find_one(
                {"$and": [{"password": password}, {"$or": [{"login": lgn}, {"name": lgn}]}]})

            if user:
                u = User(user)
                login_user(u, remember=True)
                flash("You have successfully logged in", category="success")
                return redirect("/")
            else:
                flash("User with specified login/password pair not found", category="danger")
                return redirect("/")

    def logout(self):
        logout_user()
        flash("You have successfully logged out", category="success")
        return redirect("/")
