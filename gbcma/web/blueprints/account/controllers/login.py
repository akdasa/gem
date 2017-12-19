from flask import flash, redirect, render_template, request
from flask_login import logout_user, login_user

from gbcma.db import users
from gbcma.web.app.auth import User


class LoginController:
    def login(self):
        if request.method == "GET":
            return render_template("login.html")

        elif request.method == "POST":
            data = request.form
            lgn = data.get("login", None)
            password = data.get("password", None)
            remember = data.get("remember-me", False) == "on"
            # user = users.find_one({"login": lgn, "password": password})
            print("!!!!!!!!!!!", remember)
            user = users.find_one(
                {"$and": [{"password": password}, {"$or": [{"login": lgn}, {"name": lgn}]}]})

            if user:
                u = User(user)
                login_user(u, remember=remember)
                flash("You have successfully logged in", category="success")
                return redirect("/account")
            else:
                flash("User with specified login/password pair not found", category="danger")
                return render_template("login.html")

    def logout(self):
        logout_user()
        flash("You have successfully logged out", category="success")
        return redirect("/")
