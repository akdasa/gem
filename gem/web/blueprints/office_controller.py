from flask import render_template

from gem.db import orders, services, users


class OfficeController:
    def __init__(self, name):
        self._name = name

    def _view(self):
        return {
            "office_id": self._name,
            "services": self.__load_services(self._name)
        }

    @staticmethod
    def __load_services(name):
        """Returns list of services provided by office
        :param name:
        :return: List of services"""
        return services.of(name)


class OfficeReceptionController(OfficeController):
    def __init__(self, name):
        super().__init__(name)
        self._index_template = "office/office_index.html"

    def index(self):
        return render_template(self._index_template, **self._view())

    def order(self, data, user):
        service_id = data.get("id", None)
        comment = data.get("commentary", None)
        orders.create(self._name, user.id, service_id, comment)
        return {"success": True}


class OfficeAdminController(OfficeController):
    def __init__(self, name):
        super().__init__(name)
        self._orders_template = "office/office_admin_index.html"
        self._configure_template = "office/office_admin_configure.html"

    def orders(self):
        return render_template(self._orders_template,
                               orders=self.__orders_view(), **self._view())

    def configure(self):
        return render_template(self._configure_template, **self._view())

    def add_service(self, name):
        services.create(self._name, name)
        return {"success": True}

    def __orders_view(self):
        return list(map(self.__map, orders.of(self._name)))

    def __map(self, order):
        user = users.get(order.user_id)
        service = services.get(order.service_id)
        return {
            "service": service.name,
            "comment": order.message,
            "user": user.name
        }
