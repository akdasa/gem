from munch import Munch


class Model(Munch):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
