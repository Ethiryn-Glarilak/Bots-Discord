import discord
import typing

class Generic:

    value = 0

    @staticmethod
    def generic_str():
        Generic.value += 1
        return str(Generic.value)


def get_emoji(emoji: typing.Union[discord.Emoji, discord.PartialEmoji, str]) -> discord.PartialEmoji:
    if isinstance(emoji, discord.Emoji):
        return discord.PartialEmoji(name = emoji.name, animated = emoji.animated, id = emoji.id)
    elif isinstance(emoji, discord.PartialEmoji):
        return emoji
    elif isinstance(emoji, str):
        return discord.PartialEmoji(name = emoji)
