import discord
from src.composant.composant import Composant

class Role(Composant):
    def __init__(self, id : int = None, role : discord.Role = None):
        if role is not None:
            self.discord = role
            if id is not None:
                raise ValueError("id must be not specified")
        else:
            self.discord = None
            if id is None:
                raise ValueError("id must be specified")
            self.id = id
        super().__init__()

    def check(self, other):
        return any(self == role for role in other.roles)