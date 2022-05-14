from bot.bot.import_option import Import
from extension.command_vjn import *

Import.link.update(
    {
        "commandVJN" : {
            # "bot" : BotCommandVJN,
            "parser" : ParserCommandVJN,
            "command" : CommandCommandVJN,
        },
    }
)
