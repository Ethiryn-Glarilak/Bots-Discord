from bot.valid.object.id_default import Id

class Channel(Id):
    def check(self, other):
        return self == other.channel
