from flask import Blueprint, jsonify, request
from flask_login import current_user

from .controller import BarReceptionController, BarAdminController

bar = Blueprint("bar", __name__, template_folder=".")
controller = BarReceptionController()
admin_controller = BarAdminController()


@bar.route("/")
def index():
    return controller.index()


@bar.route("/order", methods=["POST"])
def order():
    data = request.get_json(force=True)
    user = current_user
    return jsonify(controller.order(data, user))


@bar.route("/admin/orders")
def admin_orders():
    return admin_controller.orders()


@bar.route("/admin/configure", methods=["GET", "POST"])
def admin_configure():
    if request.method == "GET":
        return admin_controller.configure()
    elif request.method == "POST":
        data = request.get_json(force=True)
        service_name = data.get("name", None)
        resp = admin_controller.add_service(service_name)
        return jsonify(resp)


