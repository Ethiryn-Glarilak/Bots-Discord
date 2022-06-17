import discord
from src.composant.composant import Composant

class Channel(Composant):
    def __init__(self, id : int = None, channel : discord.TextChannel = None):
        if channel is not None:
            self.discord = channel
            if id is not None:
                raise ValueError("id must be not specified")
        else:
            self.discord = None
            if id is None:
                raise ValueError("id must be specified")
            self.id = id
        super().__init__()

    def check(self, other):
        return self == other.channel
