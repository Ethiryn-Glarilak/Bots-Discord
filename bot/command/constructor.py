from bot.command.command import *

# Import bot
from bot.command.seanren import *
from bot.command.ciaham import *

class CommandBot(CommandFunction):
    Seanren = CommandSeanren()
    Ciaham = CommandCiaham()
