from src.valid.validator_object.data import Data

class GetData(Data):

    def get_channel(self):
        return self.channel

    def get_role(self, index : int):
        if index < 0 or index >= len(self.roles):
            raise ValueError(f"Invalid role index: {index}")
        return self.roles[index]

    def get_roles(self):
        return self.roles

    def get_guild(self):
        return self.guild

    def get_user(self):
        return self.user
