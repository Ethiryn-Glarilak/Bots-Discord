import enum
from bot.interaction.composent import *

class Type(enum.IntEnum):
    BUTTON = 2
    MENU = 3
    OPTION = 5

class Interaction(list):

    def __init__(self) -> None:
        self.menu = None

    def append(self, item : dict):
        if item.get("type") < 0 or item.get("type") > 5:
            raise ValueError("Type must be between 0 and 4")
        Interaction.link[item.get("type")](self, item)

    def extend(self, items : list[dict]) :
        for item in items:
            self.append(item)

    def error(self, item : dict):
        raise NotImplementedError(f"Type {item.get('type')} is not implemented")

    def add_button(self, item: dict = None):
        if item is None:
            item = {}
        super().append(Button(**item))
        return self

    def add_option(self, item : dict = None):
        if item is None:
            item = {}
        if self.menu is None:
            self.add_menu()
        self.menu.append(Option(**item))
        return self

    def add_menu(self, item : dict = None):
        if item is None:
            item = {}
        if self.menu is not None:
            raise ValueError("Menu already exists")
        self.menu = Menu(**item)
        super().append(self.menu)
        return self

    def add_input(self, item: dict = None):
        raise NotImplementedError()
        # if item is None:
        #     item = {}
        # super().append(Input(**item))
        # return self

    link = [
        error,
        error,
        add_button,
        add_menu,
        add_input,
        add_option,
    ]

    def set_attributes_button(self):
        raise NotImplementedError()

    def get_component(self):
        return self

    def send(self, message):
        raise NotImplementedError()

    def __getattribute__(self, __name: str) -> None:
        if ("component_" in __name):
            number = __name[len("component_"):]
            if not number.isnumeric():
                raise ValueError(f"{__name} is not a component_(number)")
            return super()[int(number)]
        return super().__getattribute__(__name)

    def __str__(self):
        return list.__str__(self.get_component())

    def create_line(self):
        pass # add button on one line
