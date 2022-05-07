import discord
from bot.valid.bottom_object.data import Data
from bot.message.message import Message

class SetData(Data):

    def __init__(self, message : Message = None):
        super().__init__()
        if message is not None:
            self.set_data(message)

    def set_channel(self, channel : discord.TextChannel):
        self.channel = channel.id
        return self

    def set_role(self, role : discord.Role):
        self.roles.append(role.id)
        return self

    def set_roles(self, roles : list[discord.Role]):
        self.roles.extend(map(lambda role : role.id, roles))
        return self

    def set_server(self, server : discord.Guild):
        self.server = server.id
        return self

    def set_user(self, user : discord.User):
        self.user = user.id
        return self

    def set_data(self, message : Message):
        self.set_channel(message.channel)
        try:
            self.set_roles(message.author.roles)
        except AttributeError:
            self.set_roles([])
        self.set_server(message.guild)
        self.set_user(message.author)
        return self
