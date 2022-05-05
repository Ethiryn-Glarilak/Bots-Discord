from bot.valid.object import *
from bot.valid.bottom_object.group_object import *

class AddObject():

    def __init__(self, name = None) -> None:
        self.id : list[Id] = []
        self.object: Group = Group(name = name)
        self.function : dict = {
            "c": self.add_channel,
            "r": self.add_role,
            "s": self.add_server,
            "u": self.add_user,
        }

    def append(self, element : Id, mode : bool = None) -> None:
        group = self.object
        if mode is not None:
            group = self.object.children(mode)
        group.append(element)

    def add_channel(self, channel : int) -> None:
        self.append(Channel(channel))
        return self

    def add_role(self, role : int) -> None:
        self.append(Role(role))
        return self

    def add_server(self, server : int) -> None:
        self.append(Server(server))
        return self

    def add_user(self, user : int) -> None:
        self.append(User(user))
        return self

    def add_check(self, element : list):
        """ Valid element is good type but not valid content of element """
        if not isinstance(element, list):
            raise TypeError(f"Type {type(element)} not supported.")
        if len(element) != 2:
            raise ValueError("Must have 2 elements {int, str}[value, type]")
        if not isinstance(element[0], int):
            raise TypeError("First argument must be an int")
        if not isinstance(element[1], str):
            raise TypeError("Second argument must be a string")

    def add(self, *args) -> None:
        """ Create an exception if given element is not an instance list[int, str] """
        for element in args:
            self.add_check(element)
            self.get(element[1], self.add_error)(element[0])
        return self

    def get(self, element : str, default):
        return self.function.get(element, default)
