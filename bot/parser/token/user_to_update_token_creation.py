import enum

class DummyEnum(enum.Enum):
    a = 1

class AnotherDummyEnum(enum.Enum):
    b = 2

def chain(*iterables):
    for it in iterables:
        yield from it

def merge_enums(class_name :str, enum1, enum2, result_type = enum.Enum):
    if not (issubclass(enum1, enum.Enum) and issubclass(enum2, enum.Enum)):
        raise TypeError(f"{enum1} and {enum2} must be subclasses of Enum class")
    attrs = {attr.name : attr.value for attr in set(chain(enum1, enum2))}
    return result_type(class_name, attrs, module=__name__)

result_enum = merge_enums(class_name = "DummyEnum", enum1 = DummyEnum, enum2 = AnotherDummyEnum)

for name in result_enum:
    print(name)