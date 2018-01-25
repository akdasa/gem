from flask import render_template


_services = [
    {"id": "apple", "name": "apple juice"},
    {"id": "orange", "name": "orange juice"}
]
_orders = [

]

class OfficeController:
    def __init__(self, name):
        self._name = name
        self._services = self.__load_services(name)

    def _find_service(self, id):
        result = list(filter(lambda x: x.get("id") == id, _services))
        return result[0] if len(result) >= 1 else None

    def _view(self):
        return {
            "office_id": self._name,
            "services": self._services
        }

    @staticmethod
    def __load_services(name):
        """Returns list of services provided by office
        :param name:
        :return: List of services"""
        return _services


class OfficeReceptionController(OfficeController):
    def __init__(self, name):
        super().__init__(name)
        self._index_template = "office/office_index.html"

    def index(self):
        return render_template(self._index_template, **self._view())

    def order(self, data, user):
        service_id = data.get("id", None)
        comment = data.get("commentary", None)
        service = self._find_service(service_id)

        _orders.append({
            "service": service.get("name"),
            "user": user.name,
            "comment": comment,
            "id": service_id
        })
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
        _services.append({"id": 123, "name": name})
        return {"success": True}

    def __orders_view(self):
        return _orders