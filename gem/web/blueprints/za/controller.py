from flask import request, render_template, flash, redirect
from flask_login import current_user
from gem.db import za
from gem.web.blueprints.crud_controller import CrudController


class ZaController(CrudController):
    def __init__(self):
        super().__init__(za, namespace="za", columns=["zone", "user"])

    def _update_model(self, model, data):
        model.zone = data.get("zone", None)
        model.user = data.get("user", None)

    def display(self):
    	return render_template("za_display.html")
