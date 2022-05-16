from bot import *
from bot.interaction.interaction import Interaction
from bot.interaction.composent.option import Option
from bot.interaction.composent.menu import Menu

interaction = Interaction().add_option({"label" : "Test", "value" : "Pour voir"})


import discord_components
test = discord_components.SelectOption(label = "Test", value = "Pour voir")
menu = discord_components.Select(options = [test])

print([menu])
print(Interaction().add_option())
