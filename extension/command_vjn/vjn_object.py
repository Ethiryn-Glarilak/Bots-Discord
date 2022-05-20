import enum
import pathlib
from bot.interaction.interaction import Interaction

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

    def set_start_menu(self, bot):
        # Raccourcis bot et database
        database = bot.database.get("default")

        # Recuperation recette disponible
        event = pathlib.Path("data/689388320815710239-VJN/event-list-produit/event-load").read_text()
        path_event = pathlib.Path(f"data/689388320815710239-VJN/event-list-produit/{event}.txt")
        if not path_event.exists():
            raise ValueError(f"Event file does not exist : {path_event}")
        with open(f"data/689388320815710239-VJN/event-list-produit/{event}.txt") as file:
            product = [line.split("-")[0] for line in file.readlines()]

        # Récupération recette existante
        database.execute("SELECT * FROM product_VJN")
        database.fetchall()

        # Création composent

        self.start_menu = Interaction().add_menu(id = "menu-1", placeholder = "Choice your crêpe")
        for id, name, price in database:
            if str(id) in product:
                self.start_menu.add_option(label=f"{name.capitalize()} - {price}", value = str(id))
        if len(self.start_menu[0].options) == 0:
            self.start_menu.add_option(label = "No recipe available", value = "No recipe available")
