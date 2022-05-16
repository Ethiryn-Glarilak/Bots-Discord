import enum
from bot.interaction.generic import Generic

class Style(enum.IntEnum):
    SHORT = 1
    PARAGRAPH = 2

class Input:

    def __init__(
        self,
        id : str = None,
        style : Style = Style.SHORT,
        label : str = "Nothing",
        min : int = 1,
        max : int = 1,
        required : bool = True,
        value : str = None,
        placeholder : str = None
    ):
        self.id : str = Generic.generic_str() if id is None else id
        self.style : Style = style
        self.label : str = label
        self.min : int = min
        self.max : int = max
        self.required : bool = required
        self.value : str = value
        self.placeholder : str = placeholder

    def get_component(self):
        return self.to_dict()

    def check(self, error : bool = False):
        if len(self.id) > 100:
            if error:
                raise ValueError("Id must be at least 100 characters")
            else:
                print("Id must be at least 100 characters")
        if self.style not in [Style.SHORT, Style.PARAGRAPH]:
            if error:
                raise ValueError("Style must be either SHORT or PARAGRAPH")
            else:
                print("Style must be either SHORT or PARAGRAPH")
        if len(self.label) > 45:
            if error:
                raise ValueError("You must provide at least 45")
            else:
                print("You must provide at least 45")
        if self.min < 0 or self.min > 4000:
            if error:
                raise ValueError("Min must be at 0 4000")
            else:
                print("Min must be at 0 4000")
        if self.max < 1 or self.max > 4000:
            if error:
                raise ValueError("Max must be at 1 4000")
            else:
                print("Max must be at 1 4000")
        if self.max < self.min:
            if error:
                raise ValueError("Max not greater than min")
            else:
                print("Max not greater than min")
        if self.value is not None and len(self.value) > 4000:
            if error:
                raise ValueError("Value must be at least 4000 characters")
            else:
                print("Value must be at least 4000 characters")
        if self.placeholder is not None and len(self.placeholder) > 100:
            if error:
                raise ValueError("Placeholder must be at least 100 characters")
            else:
                print("Placeholder must be at least 100 characters")

    def to_dict(self) -> dict:
        self.check(True)
        return {
            "type" : 4,
            "custom_id" : self.id,
            "style" : self.style,
            "label" : self.label,
            "required" : self.required,
            "min_values" : self.min,
            "max_values" : self.max,
            "value" : self.value,
            "placeholder" : self.placeholder,
        }

    def __str__(self) -> str:
        return str(self.to_dict())

    def __repr__(self) -> str:
        return str(self)
