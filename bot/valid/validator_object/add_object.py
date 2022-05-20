import typing
from bot.valid.validator_object.group_object import Group
from bot.composant.channel import Channel
from bot.composant.composant import Composant
from bot.composant.role import Role
from bot.composant.guild import Guild
from bot.composant.user import User

class AddObject():

    def __init__(self, name = None) -> None:
        self.id : list[typing.Type(Composant)] = []
        self.object: Group = Group(name = name)
        self.function : dict = {
            "c": self.add_channel,
            "r": self.add_role,
            "s": self.add_guild,
            "u": self.add_user,
        }

    def append(self, element : Composant, mode : bool = None) -> None:
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

    def add_guild(self, guild : int) -> None:
        self.append(Guild(guild))
        return self

    def add_user(self, user : int) -> None:
        self.append(User(user))
        return self

    def add_error(self, error : int) -> None:
        return self

    def add_check(self, element : tuple):
        """ Valid element is good type but not valid content of element """
        if not isinstance(element, tuple):
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
