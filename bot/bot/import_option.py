import inspect
from bot.bot.ciaham import *
from bot.bot.normal import *
from bot.bot.seanren import *

class Import:

    link = {
        "Ciaham" : {
            "command" : CommandCiaham,
        },
        "Seanren" : {
            "command" : CommandSeanren,
            "parser" : ParserSeanren,
        },
        "normal" : {
            "command" : CommandNormal,
            "parser" : ParserNormal,
        },
    }

    save = {}

    def __init__(self, *args, **kwargs):
        raise NotImplementedError("Import class is not instantiated.")

    @staticmethod
    def load(bot, args):
        init = {
            "bot" : (Import.__bot_get, Import.__bot_set),
            "command" : (Import.__command_get, Import.__command_set),
            "parser" : (Import.__parser_get, Import.__parser_set),
        }

        for key, value in init.items():
            for name in args:
                list_import = Import.link.get(name, {}).get(key)
                value[0](list_import)
            value[1](bot)
            Import.save.clear()

    @staticmethod
    def __bot_get(args) -> None:
        if args is None:
            return

        filter_func = lambda method: not method[0].startswith("__")
        attributes = filter(filter_func, inspect.getmembers(args()))
        for key, value in attributes:
            Import.save[key] = value

    @staticmethod
    def __command_get(args) -> None:
        if args is None:
            return

        Import.save.update(args.additional_function)

    @staticmethod
    def __parser_get(args) -> None:
        if args is None:
            return

        filter_func = lambda method: method[0].startswith("MODE_")
        attributes = filter(filter_func, inspect.getmembers(args))
        for key, value in attributes:
            key_value = Import.save.get(key, [])
            key_value.append(value)
            Import.save[key] = key_value

    @staticmethod
    def __bot_set(bot) -> None:
        for key, value in Import.save.items():
            try:
                setattr(bot, key, value)
            except AttributeError:
                bot.log.get_logger(bot.name).error(f"key {key} cannot be changed !")

    @staticmethod
    def __command_set(bot) -> None:
        bot.command.function.update(Import.save)

    @staticmethod
    def __parser_set(bot) -> None:
        for key, value in Import.save.items():
            try:
                setattr(bot.mode, key, value)
            except AttributeError:
                bot.log.get_logger(bot.name).error(f"key {key} cannot be changed !")
