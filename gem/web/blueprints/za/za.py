from flask import Blueprint, request, render_template, flash, redirect
from flask_login import current_user

from gem.db import users

from gem.web.blueprints.za.controller import ZaController

za = Blueprint("za", __name__, template_folder=".")
controller = ZaController()


@za.route("/")
def index():
    return controller.index()


@za.route("/new", methods=["GET", "POST"])
def create():
    return controller.create(request)


@za.route("/<string:key>", methods=["GET", "POST", "DELETE"])
def update(key):
    return controller.update(request, key)

@za.route("/display")
def display():
    return controller.display()
