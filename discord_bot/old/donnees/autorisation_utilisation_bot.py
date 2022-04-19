def autorisation_utilisation_bot(message,role_autoriser):#Vérifie l'autorisation d'utilisation du bot
    roles_autorise_bool = False
    if not message.nom_serveur is None:
        for role_id_int in role_autoriser:
            if role_id_int in [role_temp.id for role_temp in message.roles]:
                roles_autorise_bool = True
                break
    return roles_autorise_bool