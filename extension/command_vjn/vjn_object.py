import enum
import json
import dotenv
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
        dotenv.load_dotenv(pathlib.Path(f"extension/command_VJN/.env{'' if bot.args.environment is None else f'-{bot.args.environment}'}"))
        self.database = bot.database.get("default")

        # Recuperation recette disponible
        event = pathlib.Path("data/689388320815710239-VJN/event-list-produit/event-load").read_text()
        path_event = pathlib.Path(f"data/689388320815710239-VJN/event-list-produit/{event}.json")
        if not path_event.exists():
            raise ValueError(f"Event file does not exist : {path_event}")
        with open(path_event, encoding="utf-8") as file:
            self.json = json.load(file)

    def set_menu(self, menu : Interaction, options : list):
        for option in options:
            menu.add_option(**option)

    def set_start_menu(self, id):
        # Récupération recette existante
        self.database.execute("SELECT * FROM product_VJN")
        self.database.fetchall()

        # Création composent
        start_menu = Interaction().add_menu(id = f"menu-start-{id}", placeholder = "Choice your crêpe")
        menu = [{"label": f"{self.database[product, 'name'].capitalize()} - {self.database[product, 'price'] if self.database[product, 'price'] != '0,00 €' else 'Gratuit'}", "value": f"crepes-{product}"} for product in [product.split("-")[0] for product in self.json.get("highlighted")] if int(product) in self.database]
        # FIXME: add choix aléatoire
        menu.extend({"label": f"{name.capitalize()}", "value": f"category-{id}"} for name, id in self.json.get("category").items())
        if self.json.get("compose", []) != []:
            menu.append({"label" : "Composer", "value" : "compose"})

        if len(menu) > 25:
            raise ValueError("To many options, max options are 25")
        if not menu:
            menu.append({"label": "empty category", "value": "error"})

        self.set_menu(start_menu, menu)
        return start_menu.add_button(label = "Annuler", style = Style.RED, id = f"annuler-start_menu-{id}")

    def set_category_menu(self, id, category):
        # Récupération recette existante
        self.database.execute("SELECT * FROM product_VJN")
        self.database.fetchall()

        # Création composent
        start_menu = Interaction().add_menu(id = f"menu-category_{category}-{id}", placeholder = "Choice your crêpe")
        menu = [{"label": f"{self.database[product, 'name'].capitalize()} - {self.database[product, 'price'] if self.database[product, 'price'] != '0,00 €' else 'Gratuit'}", "value": f"crepes-{product}"} for product in [str(product.get("id")) for product in self.json.get("product") if int(category) in product.get("category")] if int(product) in self.database]

        if len(menu) > 25:
            menu = menu[:25]
            # FIXME: Replace by a second menu
            # raise ValueError("To many options, max options are 25")
        if not menu:
            menu.append({"label": "empty category", "value": "error"})

        self.set_menu(start_menu, menu)
        return start_menu.add_interaction(
            Interaction()
                .add_button(label = "Retour", style = Style.GREY, id = f"retour-start-{id}")
                .add_button(label = "Annuler", style = Style.RED, id = f"annuler-category_menu-{id}")
        )

    def set_compose_menu(self, id, default : list[str]):
        # Récupération recette existante
        self.database.execute("SELECT * FROM ingredient_VJN")
        self.database.fetchall()

        # Création composent
        menu = [{"label": f"{self.database[product, 'name'].capitalize()} - {self.database[product, 'price'] if self.database[product, 'price'] != '0,00 €' else 'Gratuit'}", "value": f"ingredient-{product}", "default": product in default} for product in [str(product) for product in self.json.get("compose").values()] if int(product) in self.database]

        if len(menu) > 25:
            menu = menu[:25]
            # FIXME: Replace by a second menu
            # raise ValueError("To many options, max options are 25")
        if not menu:
            menu.append({"label": "empty category", "value": "error"})

        start_menu = Interaction().add_menu(id = f"menu-ingredient-{id}", placeholder = "Choice your crêpe", max = len(menu))
        self.set_menu(start_menu, menu)
        return start_menu.add_interaction(
            Interaction()
                .add_button(label = "Valider", style = Style.GREEN, id = f"valid-compose-{id}")
                .add_button(label = "Retour", style = Style.GREY, id = f"retour-start-{id}")
                .add_button(label = "Annuler", style = Style.RED, id = f"annuler-compose_menu-{id}")
        )

    def set_check_command(self, id, origin):
        return Interaction()\
            .add_interaction(
                Interaction()
                    .add_button(label = "Valider", style = Style.GREEN, id = f"valid-command-{id}")
                    .add_button(label = "Retour", style = Style.GREY, id = f"retour-{origin}-{id}")
                    .add_button(label = "Annuler", style = Style.RED, id = f"annuler-check_command-{id}")
            )

    def set_paiement_command(self, id):
        return Interaction()\
            .add_interaction(
                Interaction()
                    .add_button(label = "Valider", style = Style.GREEN, id = f"valid-paiement-{id}")
                    .add_button(label = "Annuler", style = Style.RED, id = f"annuler-paiement-{id}")
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
                    .add_button(label = "Annuler", style = Style.RED, id = f"annuler-after_assigned-{id}")
            )

    def set_livrer(self, id):
        return Interaction().add_button(label = "Livrer", style = Style.GREEN, id = f"valid-livrer-{id}")
