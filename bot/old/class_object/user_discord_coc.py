caractere_separation = "۩"

class compte_coc:
    def __init__(self, *args, **kwargs):
        msg_erreur = ""
        try:
            if kwargs["discord_ID"].isnumeric():
                self.discord_ID = int(kwargs["discord_ID"])
        except:
            msg_erreur = "cf discord_ID"
        try:
            self.discord_nom_user = kwargs["discord_nom_user"]
        except:
            msg_erreur = "cf discord_nom_user"
        try:
            self.coc_ID = kwargs["coc_ID"]
        except:
            msg_erreur = "cf coc_ID"
        try:
            self.coc_nom_user = kwargs["coc_nom_user"]
        except:
            msg_erreur = "cf coc_nom_user"
        if msg_erreur != "":
            print("Erreur nombre et ou nom d'argument invalide,",msg_erreur)

    def clans_compte(self, *args, **kwargs):
        try:
            self.clans_ID = kwargs["clansID"]
        except:
            print("Erreur nombre et ou nom d'argument invalide, cf clans_ID")
        try:
           self.clans_nom = kwargs["clansnom"]
        except:
            print("Erreur nombre et ou nom d'argument invalide, cf clans_htag")

    def info_compte_coc(self, *args, **kwargs):
        attribut_str = ""
        if "all" in args:
            for attribut in self.__dict__.values():
                attribut_str += str(attribut) + caractere_separation
            return (self.discord_ID,attribut_str[0:len(attribut_str)-1],caractere_separation)
        elif "select" in args:
            print("Mode select non fonctionnel")
            """
            for attribut in self.__dict__:
                if attribut in args:
                    attribut_str += str(self.attribut) + caractere_separation
            return (self.discord_ID,attribut_str[0:len(attribut_str)-1],caractere_separation)
            """
        else:
            print("Erreur argument manquant, select ou all")