import discord
from src.composant.composant import Composant

class Guild(Composant):
    def __init__(self, id : int = None, guild : discord.Guild = None):
        if guild is not None:
            self.discord = guild
            if id is not None:
                raise ValueError("id must be not specified")
        else:
            self.discord = None
            if id is None:
                raise ValueError("id must be specified")
            self.id = id
        super().__init__()

    def check(self, other):
        return self == other.guild
