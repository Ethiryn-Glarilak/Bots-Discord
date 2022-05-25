from ast import In
import enum
import json
import pathlib
from bot.interaction.interaction import Interaction
from bot.interaction.composent.button import Style

class Status(enum.IntEnum):
    COMMAND = 10
    PAYMENT_REQUIRED = 11
    PAYMENT_IN_PROGRESS = 12
    FILE_ATTENTE = 13
    PREPARATION_0 = 0
    PREPARATION_1 = 1
    PREPARATION_2 = 2
    PREPARATION_3 = 3
    PREPARATION_4 = 4
    PREPARATION_5 = 5
    PREPARATION_6 = 6
    PREPARATION_7 = 7
    PREPARATION_8 = 8
    PREPARATION_9 = 9
    READY = 14
    FINISH = 15

class VJNObject:

    def __init__(self, bot):
        # Raccourcis bot et database
        self.database = bot.database.get("default")

        # Recuperation recette disponible
        event = pathlib.Path("data/689388320815710239-VJN/event-list-produit/event-load").read_text()
        path_event = pathlib.Path(f"data/689388320815710239-VJN/event-list-produit/{event}.json")
        if not path_event.exists():
            raise ValueError(f"Event file does not exist : {path_event}")
        with open(path_event, encoding="utf-8") as file:
            self.json = json.load(file)

        self.set_start_menu()
        self.set_check_command()

    def set_menu(self, menu : Interaction, options : list):
        for option in options:
            menu.add_option(**option)

    def set_start_menu(self):
        # Récupération recette existante
        self.database.execute("SELECT * FROM product_VJN")
        self.database.fetchall()

        # Création composent
        self.start_menu = Interaction().add_menu(id = "menu-1", placeholder = "Choice your crêpe")
        menu = [{"label": f"{self.database[product, 'name'].capitalize()} - {self.database[product, 'price']}", "value": f"crepes-{product}"} for product in [product.split("-")[0] for product in self.json.get("highlighted")] if int(product) in self.database]
        # FIXME: add choix aléatoire
        menu.extend({"label": f"{name.capitalize()}", "value": f"category-{id}"} for name, id in self.json.get("category").items())
        if self.json.get("compose", False):
            menu.append({"label" : "Composer", "value" : "compose"})

        if len(menu) > 25:
            raise ValueError("To many options, max options are 25")

        self.set_menu(self.start_menu, menu)

    def set_check_command(self, id):
        return Interaction()\
            .add_interaction(
                Interaction()
                    .add_button(label = "Valider", style = Style.GREEN, id = "valid-command")
                    # FIXME: ajouter bouton pour revenir en arrière
                    # .add_button(label = "Retour", style = Style.GREY, id = "retour")
                    # FIXME: ajouter bouton pour annuler
                    # .add_button(label = "Annuler", style = Style.RED, id = f"annuler-assigned-{id}")
            )

    def set_paiement_command(self, id):
        return Interaction()\
            .add_interaction(
                Interaction()
                    .add_button(label = "Valider", style = Style.GREEN, id = f"valid-paiement-{id}")
                    .add_button(label = "Annuler", style = Style.RED, id = f"annuler-assigned-{id}")
            )

    def set_assignment(self, id):
        cooks = Interaction()
        for i in range(min(self.json.get("cooks"), 10)):
            cooks.add_button(label = f"Cooks {i}", style = Style.GREY, id = f"assigned-{id}-{i}")
        return Interaction()\
            .add_interaction(cooks)\
            .add_button(label = "Annuler", style = Style.RED, id = f"annuler-assigned-{id}")

    def set_after_assignment(self, id):
        return Interaction()\
            .add_interaction(
                Interaction()
                    .add_button(label = "Valider", style = Style.GREEN, id = f"valid-assigned-{id}")
                    .add_button(label = "Modifier", style = Style.BLUE, id = f"modifier-assigned-{id}")
                    .add_button(label = "Annuler", style = Style.RED, id = f"annuler-assigned-{id}")
            )

    def set_livrer(self, id):
        return Interaction().add_button(label = "Livrer", style = Style.GREEN, id = f"valid-livrer-{id}")
