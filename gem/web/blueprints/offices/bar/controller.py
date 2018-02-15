from gem.web.blueprints.office_controller import OfficeReceptionController, OfficeAdminController


class BarReceptionController(OfficeReceptionController):
    def __init__(self):
        super().__init__("bar")


class BarAdminController(OfficeAdminController):
    def __init__(self):
        super().__init__("bar")
