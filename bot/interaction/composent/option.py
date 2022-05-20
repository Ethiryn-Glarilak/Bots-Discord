from bot.interaction.generic import Generic
from bot.interaction.generic import get_emoji

class Option:

    def __init__(
        self,
        label : str = "Nothing",
        value : str = None,
        description : str = None,
        emoji = None,
        default : bool = False,
    ):
        self.label : str = label
        self.value : str = Generic.generic_str() if value is None else value
        self.description : str = description
        self.emoji : str = None if emoji is None else get_emoji(emoji)
        self.default : bool = default

    def get_component(self):
        return self.to_dict()

    def check(self, error : bool = False):
        if len(self.label) > 100:
            if error:
                raise ValueError("Label must be at least 100 characters")
            else:
                print("Label must be at least 100 characters")
        if len(self.value) > 100:
            if error:
                raise ValueError("Value must be at least 100 characters")
            else:
                print("Value must be at least 100 characters")
        if self.description is not None and len(self.description) > 100:
            if error:
                raise ValueError("Description must be at least 100 characters")
            else:
                print("Description must be at least 100 characters")

    def to_dict(self) -> dict:
        self.check(True)
        data = {
            "label": self.label,
            "value": self.value,
            "description": self.description,
            "default": self.default,
        }
        if self.emoji is not None:
            data["emoji"] = self.emoji.to_dict()
        return data

    def __str__(self) -> str:
        return str(self.to_dict())

    def __repr__(self) -> str:
        return str(self)
