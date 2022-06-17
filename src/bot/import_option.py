import inspect
from src.bot.ciaham import *
from src.bot.normal import *
from src.bot.seanren import *
from src.data.postgres import DataBase

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
            "ready" : (Import.__ready_get, Import.__ready_set),
            "command" : (Import.__command_get, Import.__command_set),
            "parser" : (Import.__parser_get, Import.__parser_set),
            "interaction" : (Import.__interaction_get, Import.__interaction_set),
            "postgres" : (Import.__postgres_get, Import.__postgres_set),
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
    def __bot_set(bot) -> None:
        for key, value in Import.save.items():
            try:
                setattr(bot, key, value)
            except AttributeError:
                bot.log.get_logger(bot.name).error(f"key {key} cannot be changed !")

    @staticmethod
    def __ready_get(args) -> None:
        if args is None:
            return
        Import.save.update(args.additional_function)

    @staticmethod
    def __ready_set(bot) -> None:
        bot.ready.update(Import.save)

    @staticmethod
    def __command_get(args) -> None:
        if args is None:
            return
        Import.save.update(args.additional_function)

    @staticmethod
    def __command_set(bot) -> None:
        bot.command.function.update(Import.save)

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
    def __parser_set(bot) -> None:
        for key, value in Import.save.items():
            try:
                setattr(bot.mode, key, value)
            except AttributeError:
                bot.log.get_logger(bot.name).error(f"key {key} cannot be changed !")

    @staticmethod
    def __interaction_get(args) -> None:
        if args is None:
            return
        Import.save.update(args.additional_function)

    @staticmethod
    def __interaction_set(bot) -> None:
        bot.interaction.function.update(Import.save)

    @staticmethod
    def __postgres_get(args) -> None:
        if args is None:
            return
        Import.save[args.__name__] = args()

    @staticmethod
    def __postgres_set(bot) -> None:
        for key, value in Import.save.items():
            postgres = bot.database.get("default") if value.info is None else DataBase(**value.info)
            bot.database[key] = postgres
            value.db = postgres
            value.start(bot)
