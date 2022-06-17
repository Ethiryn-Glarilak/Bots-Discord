import enum
from src.interaction.generic import Generic
from src.interaction.generic import get_emoji

class Style(enum.IntEnum):
    BLUE = 1
    GREY = 2
    GREEN = 3
    RED = 4
    URL = 5

class Button:

    def __init__(
        self,
        style : int = Style.BLUE,
        label : str = "Nothing",
        emoji = None,
        id : str = None,
        url : str = None,
        disabled : bool = False,
    ):
        self.style : int = style
        self.label : str = label
        self.emoji : str = None if emoji is None else get_emoji(emoji)
        self.id : str = Generic.generic_str() if id is None else id
        self.url : str = url
        self.disabled : bool = disabled

    def get_component(self):
        return self.to_dict()

    def check(self, error : bool = False):
        if self.style < 1 or self.style > 5:
            if error:
                raise ValueError("You must choices style in class Style")
            else:
                print("You must choices style in class Style")
        if len(self.label) > 80:
            if error:
                raise ValueError("Label must be at least 80 characters")
            else:
                print("Label must be at least 80 characters")
        if len(self.id) > 100:
            if error:
                raise ValueError("Id must be at least 100 characters")
            else:
                print("Id must be at least 100 characters")

    def to_dict(self) -> dict:
        self.check(True)
        data = {
            "type": 2,
            "style": self.style,
            "label": self.label,
            "custom_id": self.id,
            "url": self.url if self.style == Style.URL else None,
            "disabled": self.disabled,
        }
        if self.emoji is not None:
            data["emoji"] = self.emoji.to_dict()
        return data

    def __str__(self) -> str:
        return str(self.to_dict())

    def __repr__(self) -> str:
        return str(self)
