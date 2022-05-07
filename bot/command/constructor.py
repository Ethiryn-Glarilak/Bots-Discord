from bot.command.command import CommandFunction

# Import bot
from bot.command.ciaham import CommandCiaham
from bot.command.seanren import CommandSeanren

class CommandBot(CommandFunction):
    Seanren = CommandSeanren()
    Ciaham = CommandCiaham()
