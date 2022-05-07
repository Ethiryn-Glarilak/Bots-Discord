from bot.valid.bottom_object.add_object import AddObject
from bot.valid.bottom_object.get_data import GetData
from bot.valid.bottom_object.set_data import SetData

class Validator(AddObject, GetData, SetData):

    def __init__(self, **kwargs):
        AddObject.__init__(self, **kwargs)
        GetData.__init__(self, **kwargs)
        SetData.__init__(self, **kwargs)

    def check(self):
        return self.object.check(self)
