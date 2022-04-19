def recuperation_msg(message, majuscule = False):#Récuperer le message sous forme d'un dictionnaire contenant la commande et une liste avec les parametres
    msg_str = message.content
    msg_list = msg_str.split()
    try:
        if majuscule == True:
            commande = msg_list[0]
        else:
            commande = msg_list[0].lower()
        parametre = msg_list[0:]
    except:
        commande = ""
        parametre = ""
    return commande, parametre

class message_info():

    __slots__ = ("message", "nom_bot",
                 "auteur","id_auteur","id_auteur_str","auteur_str",
                 "roles",
                 "heure_c","heure_c_str",
                 "nom_serveur","id_serveur","id_serveur_str",
                 "nom_salon",
                 "commande","_parametre")

    def __init__(self, message, MAJ = False, nom = "Nom Bot (Oublie)"):
        self.message = message.content #message
        self.nom_bot = nom
        self.auteur = message.author #user_name
        self.id_auteur= message.author.id #user_id_int
        self.roles = message.author.roles #user_roles
        self.heure_c = message.created_at #msg_date_created_int
        self.nom_serveur= message.guild.name #serveur_str
        self.id_serveur = message.guild.id #serveur_id_int
        self.nom_salon = message.channel.name #salon_name_str
        self.commande, self._parametre = recuperation_msg(message, MAJ)

#A vérifier
        self.id_auteur_str = str(message.author.id) #user_id_str
        self.auteur_str= str(message.author) #user_name_str
        self.heure_c_str = str(message.created_at) #msg_date_created_str
        self.id_serveur_str = str(message.guild.id) #serveur_id_str

    def __str__(self):
        return self.message

    def __repr__(self):
        return f"Message : Auteur({self.auteur}), Contenu({self.message})"

    def __getattr__(self, attribut):
        print(f"L'attribut {attribut} n'existe pas.")

    def __delattr__(self, attribut):
        raise AttributeError("On ne peut pas supprimer les attributs")

    def __getitem__(self, index):
        return self.index

    def __setitem__(self, index, valeur):
        self.index = valeur

    def _get_parametre(self):
        return f"Commande : \"{self.commande}\" parametre : {self._parametre}"

    parametre = property(_get_parametre)