from src.interaction.generic import Generic

class Menu:
# Si ajout de notre propre overload Menu peut hériter de list pour contenir les options
    def __init__(
        self,
        id : str = None,
        placeholder : str = None,
        min : int = 1,
        max : int = 1,
        disabled : bool = False
    ):
        self.id : str = Generic.generic_str() if id is None else id
        self.placeholder : str = placeholder
        self.options : list = []
        self.min : int = min
        self.max : int = max
        self.disabled : bool = disabled

    def append(self, item):
        if len(self.options) > 24:
            raise ValueError("You must provide at least 25")
        self.options.append(item)

    def extend(self, item):
        if len(self.options) + len(item) > 25:
            raise ValueError("You must provide at least 25")
        self.options.extend(item)

    def get_component(self):
        return self.to_dict()

    def check(self, error : bool = False):
        if len(self.id) > 100:
            if error:
                raise ValueError("Id must be at least 100 characters")
            else:
                print("Id must be at least 100 characters")
        if len(self.options) <= 0:
            if error:
                raise ValueError("You must provide at least 1")
            else:
                print("You must provide at least 1")
        if len(self.options) > 25:
            if error:
                raise ValueError("You must provide at least 25")
            else:
                print("You must provide at least 25")
        if self.placeholder is not None and len(self.placeholder) > 150:
            if error:
                raise ValueError("Placeholder must be at least 150 characters")
            else:
                print("Placeholder must be at least 150 characters")
        if self.min < 0 or self.min > 25:
            if error:
                raise ValueError("Min must be at 0 25")
            else:
                print("Min must be at 0 25")
        if self.max < 1 or self.max > 25:
            if error:
                raise ValueError("Max must be at 1 25")
            else:
                print("Max must be at 1 25")
        if self.max < self.min:
            if error:
                raise ValueError("Max not greater than min")
            else:
                print("Max not greater than min")

    def to_dict(self) -> dict:
        self.check(True)
        return {
            "type": 3,
            "custom_id": self.id,
            "options": list(map(lambda option : option.to_dict(), self.options)),
            "placeholder": self.placeholder,
            "min_values": self.min,
            "max_values": self.max,
            "disabled": self.disabled,
        }

    def __str__(self) -> str:
        return str(self.to_dict())

    def __repr__(self) -> str:
        return str(self)
