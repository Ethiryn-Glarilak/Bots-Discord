from bot.valid.bottom_object import *

class Validator(AddObject, GetData, SetData):

    def check(self):
        return self.object.check(self)
 
    # def check(self) -> bool:  # sourcery skip: merge-duplicate-blocks
    #     for element in self.id:
    #         if isinstance(element, Channel):
    #             if getattr(self, "channel", None) is None:
    #                 raise ValueError("Channel not defined.")
    #             if element != self.channel:
    #                 return False
    #         elif isinstance(element, Role):
    #             if getattr(self, "role", None) is None:
    #                 raise ValueError("Role not defined.")
    #             if element != self.role:
    #                 return False
    #         elif isinstance(element, Server):
    #             if getattr(self, "server", None) is None:
    #                 raise ValueError("Server not defined.")
    #             if element != self.server:
    #                 return False
    #         elif isinstance(element, User):
    #             if getattr(self, "user", None) is None:
    #                 raise ValueError("User not defined")
    #             if element != self.user:
    #                 return False
    #     return True

    # def add_or(self):
    #     element = self.id
    #     while isinstance(element[-1], list):
    #         element = element[-1]

    #     element.append("or")

    # def add_not(self):
    #     print("verifier la positionnement")
    #     element = self.id
    #     while isinstance(element[-1], list):
    #         element = element[-1]

    #     element.insert(0, "not")

    # def add_level(self):
    #    pass
