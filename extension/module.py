from bot.bot.import_option import Import
from extension.vjn_command import *
from extension.command_vjn import *

Import.link.update(
    {
        "commandVJN" : {
            "bot" : BotCommandVJN,
            "parser" : ParserCommandVJN,
            "command" : CommandCommandVJN,
            "interaction" : InteractionCommandVJN,
            "postgres" : PostgresCommandVJN,
        },
        "VJN_Command" : {
            "command" : CommandVJNCommand,
            "parser" : ParserVJNCommand,
        },
    }
)
