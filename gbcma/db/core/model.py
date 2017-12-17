from munch import Munch


class Model(Munch):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def id(self):
        return self.get("_id")


class Proposal(Model):
    pass
