from flask import Blueprint, render_template, request, jsonify, flash, redirect
from flask_login import login_required

from gbcma.db.users import UsersRepository
from gbcma.web.app.auth import has_permission, have_no_permissions

users = Blueprint("users", __name__, template_folder=".")
rep = UsersRepository()


@users.route("/")
@login_required
def index():
    """Shows list of users."""
    if has_permission("users.read"):
        ul = rep.all()  # get all users to show
        return render_template("users_index.html", users=ul)
    else:
        return have_no_permissions()


@users.route("/new", methods=["GET", "POST"])
@login_required
def create():
    """Creates new user."""
    if not has_permission("users.create"):
        return have_no_permissions()

    if request.method == "GET":
        return render_template("users_new.html", user=None)

    elif request.method == "POST":
        doc = __form_to_dict(request.form, {})
        rep.insert(doc)

        flash("User was successfully created", category="success")
        return redirect("/users")


@users.route("/<string:key>", methods=["GET", "POST", "DELETE"])
@login_required
def update(key):
    """Shows user."""
    if request.method == "GET":
        if has_permission("users.read"):
            return render_template("users_view.html", user=rep.get(key))
        else:
            return have_no_permissions()

    elif request.method == "POST":
        if has_permission("users.update"):
            d = rep.get(key)
            doc = __form_to_dict(request.form, d)
            rep.save(doc)

            flash("User was successfully updated", category="success")
            return redirect("/users")
        else:
            return have_no_permissions()

    if request.method == "DELETE":
        if has_permission("users.delete"):
            rep.delete(key)
            return jsonify({"success": True})
        else:
            return jsonify({"success": False})


def __form_to_dict(form, d):
    d.update({
        "name": form.get("name", None),
        "login": form.get("login", None),
        "password": form.get("password", ""),
        "permissions": list(filter(None, str.split(form.get("permissions", ""), " ")))
    })
    return d