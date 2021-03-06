from src.valid.validator_object import *

class Validator(AddObject, GetData, SetData):

    def __init__(self, **kwargs):
        AddObject.__init__(self, **kwargs)
        GetData.__init__(self, **kwargs)
        SetData.__init__(self, **kwargs)

    def check(self):
        return self.object.check(self)
