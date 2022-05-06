from bot import Data, Message

class SetData(Data):

    def __init__(self, message : Message = None):
        super().__init__()
        if message is not None:
            self.set_data(message)

    def set_channel(self, channel : int):
        self.channel = channel
        return self

    def set_role(self, role : int):
        self.roles.append(role)
        return self

    def set_roles(self, roles : list[int]):
        self.roles.extend(map(lambda role : role.id, roles))
        return self

    def set_server(self, server : int):
        self.server = server
        return self

    def set_user(self, user : int):
        self.user = user
        return self

    def set_data(self, message : Message):
        self.set_channel(message.message.channel)
        self.set_roles(message.message.author.roles)
        self.set_server(message.message.guild)
        self.set_user(message.message.author.id)
        return self
