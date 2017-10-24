from flask import render_template, flash, redirect, jsonify
from inflection import singularize

from gbcma.web.app.auth import has_permission, access_denied


class CrudController:
    def __init__(self, repository, namespace=None):
        self._repository = repository
        self._columns = []
        self._namespace = namespace
        self._model_name = singularize(self._namespace)
        self._actions = []
        self._js = []

        if namespace:
            self._permission = namespace
            self._form = "{}_form.html".format(namespace)
            self._url = namespace

    def register_js(self, name):
        self._js.append(name)

    def register_action(self, css_class, icon):
        self._actions.append({"css_class": css_class, "icon": icon})

    def index(self):
        """Shows list of models."""
        if not self._has_permission("read"):
            return access_denied()

        models = self._repository.all()
        return render_template("crud/index.html", models=models, fields=self._columns, **self.__options())

    def create(self, request):
        """Creates new user."""
        if not self._has_permission("create"):
            return access_denied()

        if request.method == "GET":
            return render_template("crud/new.html", **self.__options())

        elif request.method == "POST":
            doc = self._form_to_dict(request.form, {})
            self._repository.insert(doc)

            flash("{} was successfully created".format(self._namespace), category="success")
            return redirect("/" + self._url)

    def update(self, request, key):
        """Shows user."""
        if request.method == "GET":
            if self._has_permission("read"):
                entity = self._repository.get(key)
                return render_template("crud/view.html", model=entity, **self.__options(), **self._extend(entity))
            else:
                return access_denied()

        elif request.method == "POST":
            if self._has_permission("update"):
                d = self._repository.get(key)
                doc = self._form_to_dict(request.form, d)
                self._repository.save(doc)

                flash("{} was successfully updated".format(self._namespace), category="success")
                return redirect("/" + self._url)
            else:
                return access_denied()

        if request.method == "DELETE":
            if self._has_permission("delete"):
                self._repository.delete(key)
                return jsonify({"success": True})
            else:
                return jsonify({"success": False})

    def _form_to_dict(self, form, d):
        return {}

    def _has_permission(self, kind):
        # No permission specified, so everything is allowed
        if not self._permission:
            return True
        else:
            return has_permission("{}.{}".format(self._permission, kind))

    def __options(self):
        return {
            "form": self._form,
            "active_page": self._namespace,
            "url": self._url,
            "model_name": self._model_name,
            "namespace": self._namespace,
            "actions": self._actions,
            "js": self._js,
            "show_actions": self._has_permission("delete"),
            "show_delete": self._has_permission("delete"),
            "show_create": self._has_permission("create"),
        }

    def _extend(self, model):
        return {}
