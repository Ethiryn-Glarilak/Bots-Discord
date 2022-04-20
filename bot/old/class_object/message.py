import discord

class Message(discord.message.Message):

    def __init__(self) -> None:
        super().__init__()

    def __str__(self) -> str:
        return ""

    def __repr__(self):
        return f"Message : Auteur({self.auteur}), Contenu({self.message})"

    def __getattr__(self, attribut):
        print(f"L'attribut {attribut} n'existe pas.")

    def __getitem__(self, index):
        return self.index

    def __setitem__(self, index, valeur):
        self.index = valeur

    def _get_parametre(self):
        return f"Commande : \"{self.commande}\" parametre : {self._parametre}"

    parametre = property(_get_parametre)