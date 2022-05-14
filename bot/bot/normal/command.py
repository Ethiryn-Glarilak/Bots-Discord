import os
import platform
from bot.parser.token.token_type import TokenType
from bot.valid.default import DefaultValidator

async def reboot(message) -> None:
    if DefaultValidator.creator(message).check():
        try:
            await message.bot.get_channel(966322896014307398).send(f"Command reboot of {message.bot.name}.")
            await message.bot.close()
        except Exception:
            print("Exception")
        finally:
            if platform.system() == "Windows":
                os.system(f"py -3 {message.bot.name}.py")
            elif platform.system() == "Linux":
                os.system(f"python3 {message.bot.name}.py")
            else:
                message.bot.log.get_logger("command").error(f"os not supported : {platform.system()}")
    else:
        await message.bot.get_channel(966322896014307398).send(f"User {message.author} use command reboot but not authorized.")

async def close(message) -> None:
    if DefaultValidator.creator(message).check():
        await message.bot.get_channel(966322896014307398).send(f"Command close of {message.bot.name}.")
        await message.bot.close()
    else:
        await message.bot.get_channel(966322896014307398).send(f"User {message.author} use command close but not authorized.")

class CommandNormal:

    additional_function = {
        TokenType.TOKEN_CLOSE.name : close,
        TokenType.TOKEN_REBOOT.name : reboot,
    }

