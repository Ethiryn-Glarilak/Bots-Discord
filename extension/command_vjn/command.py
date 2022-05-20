from bot.command.command import Command
from bot.interaction.interaction import Interaction
from bot.interaction.composent.button import Style
from bot.parser.token.token_type import TokenType
from bot.valid.default import DefaultValidator

async def refresh(message) -> None:
    if DefaultValidator.creator(message).check():
        channel = message.bot.get_channel(972454299789557860)
        async for element in channel.history():
            await element.delete()
        components = Interaction().add_button(label = "Commander", style = Style.GREEN, id = "commander", emoji = "✅")
        await channel.send("Clicker et rendez-vous dans tes DM avec moi", components=components)
        message.bot.vjn_object.set_start_menu(message.bot)

# async def none(message) -> None:
#     if DefaultValidator.channel(message, [972454299789557860]).check() \
#         and not DefaultValidator.user(message, [message.bot.user.id]):
#         await message.delete()
#         # Add log
#     else:
#         await Command().none(message)

async def example(message) -> None:
    if not DefaultValidator.creator(message).check():
        return
    channel = message.bot.get_channel(977246505738076231)
    async for element in channel.history():
        await element.delete()

    # 0.
    await channel.send("Tout fonctionne (quand le bot est en ligne) :arrow_down:")

    # 1.
    await channel.send("Clicker et rendez-vous dans tes DM avec moi", components=Interaction().add_button(label = "Commander", style = Style.GREEN, id = "test_commander"))

    # 2.
    await channel.send(
        components=Interaction()
            .add_menu(id = "test-menu-1", placeholder = "Que voulez-vous ?")
            .add_option(label = "Crêpe sucre", value = "crepes-1", emoji = "🧁")
            .add_option(label = "Crêpe nutella", value = "crepes-2")
            .add_option(label = "Crêpe nutella banane", value = "crepes-3")
            .add_option(label = "Crêpe jambon œuf fromage", value = "crepes-4", emoji = "🧁")
            .add_option(label = "Barbe à papa", value = "barbe-a-papa")
            .add_option(label = "Crêpe thon emmental raclette œuf", value = "crepes-aléatoire")
            .add_option(label = "Crêpe Bière", value = "catégorie-1")
            .add_option(label = "Crêpe Sucré", value = "catégorie-2", emoji = "🧁")
            .add_option(label = "Crêpe Poulet", value = "catégorie-3")
            .add_option(label = "Composer", value = "composition")
            .add_button(label = "Annuler", style = Style.RED, id = "annuler", emoji = "❎")
    )

    # 2.2
    await channel.send(
        components=Interaction()
            .add_menu(id = "test-menu-1", placeholder = "Que voulez-vous dans la catégorie Bière ?")
            .add_option(label = "Crêpe Bière sucre", value = "crepes-1-bière")
            .add_option(label = "Crêpe Bière nutella", value = "crepes-2-bière")
            .add_option(label = "Crêpe Bière nutella banane", value = "crepes-3-bière", emoji = "🧁")
            .add_option(label = "Crêpe Bière jambon œuf fromage", value = "crepes-4-bière")
            .add_option(label = "Crêpe Bière thon emmental raclette œuf", value = "crepes-aléatoire-bière")
            .add_interaction(
                Interaction()
                    .add_button(label = "Retour", style = Style.GREY, id = "retour")
                    .add_button(label = "Annuler", style = Style.RED, id = "annuler", emoji = "❎")
            )
    )

    # 2.3.1
    await channel.send(
        "Composer votre commande :",
        components=Interaction()
            .add_button(label = "Crêpes", id = "crepes_composition")
            .add_button(label = "Barbe à papa", id = "barbe_a_papa_composition")
            .add_interaction(
                Interaction()
                    .add_button(label = "Retour", style = Style.GREY, id = "retour")
                    .add_button(label = "Annuler", style = Style.RED, id = "annuler", emoji = "❎")
            )
    )


    # 2.3.2.0
    await channel.send(
        "Composer votre crêpe :",
        components=Interaction()
            .add_button(label = "Pate", id = "pate_composition")
            .add_button(label = "Garniture", id = "garniture_composition")
            .add_interaction(
                Interaction()
                    .add_button(label = "Valider", id = "valider", style = Style.GREEN, disabled = True, emoji = "✅")
                    .add_button(label = "Retour", style = Style.GREY, id = "retour")
                    .add_button(label = "Annuler", style = Style.RED, id = "annuler", emoji = "❎")
            )
    )

    # 2.3.2.1
    await channel.send(
        "Composer votre crêpe :",
        components=Interaction()
            .add_button(label = "Pate", id = "pate_composition")
            .add_button(label = "Garniture", id = "garniture_composition")
            .add_interaction(
                Interaction()
                    .add_button(label = "Valider", style = Style.GREEN, id = "valider", emoji = "✅")
                    .add_button(label = "Retour", style = Style.GREY, id = "retour")
                    .add_button(label = "Annuler", style = Style.RED, id = "annuler", emoji = "❎")
            )
    )

    # 2.3.2.2
    await channel.send(
        "Composer votre crêpe :",
        components=Interaction()
            .add_menu(id = "test-menu-1", placeholder = "Que voulez-vous comme pate ?")
            .add_option(label = "Bière", value = "bière")
            .add_option(label = "Nature", value = "nature")
            .add_option(label = "Sucré", value = "sucré", emoji = "🧁")
            .add_option(label = "Salé", value = "salé")
            .add_option(label = "Vegan", value = "vegan")
            .add_interaction(
                Interaction()
                    .add_button(label = "Retour", style = Style.GREY, id = "retour")
                    .add_button(label = "Annuler", style = Style.RED, id = "annuler", emoji = "❎")
            )
    )

    # 2.3.3
    await channel.send(
        "Composer votre barbe à papa :",
        components=Interaction()
            .add_menu(id = "test-menu-1", placeholder = "Quelle couleur voulez-vous pour votre barbe à papa ?")
            .add_option(label = "Bleu", value = "bleu", emoji = "🔵")
            .add_option(label = "Rouge", value = "rouge", emoji = "🔴")
            .add_option(label = "Verte", value = "vert", emoji = "🟢")
            .add_interaction(
                Interaction()
                    .add_button(label = "Retour", style = Style.GREY, id = "retour")
                    .add_button(label = "Annuler", style = Style.RED, id = "annuler", emoji = "❎")
            )
    )

    # 3.
    await channel.send(
        "N*6 : Olivier C. [BDE - EPTV - VJN]#9175\nCrêpes sucre 1€ x5 = 5€",
        components=Interaction()
            .add_interaction(
                Interaction()
                    .add_button(label = "Valider", style = Style.GREY, id = "valider", emoji = "✅")
                    .add_button(label = "Annuler", style = Style.RED, id = "annuler", emoji = "❎")
            )
    )

    # 4.
    await channel.send(
        "N*6 : Olivier C. [BDE - EPTV - VJN]#9175\nCrêpe sucre",
        components=Interaction()
            .add_interaction(
                Interaction()
                    .add_button(label = "Préparateur 1", style = Style.GREY, id = "preparation_1")
                    .add_button(label = "Préparateur 2", style = Style.GREY, id = "preparation_2")
                    .add_button(label = "Préparateur 3", style = Style.GREY, id = "preparation_3")
            )
            .add_button(label = "Annuler", style = Style.RED, id = "annuler", emoji = "❎")
    )

    # 5.
    await channel.send(
        "N*6 : Olivier C. [BDE - EPTV - VJN]#9175\nCrêpe sucre -> 3",
        components=Interaction()
            .add_interaction(
                Interaction()
                    .add_button(label = "Valider", style = Style.GREEN, id = "valider", emoji = "✅")
                    .add_button(label = "Modifier", style = Style.GREY, id = "modifier")
                    .add_button(label = "Annuler", style = Style.RED, id = "annuler", emoji = "❎")
            )
    )

    # 6.
    await channel.send(
        "Commande prête : n*6 : Crêpe sucre",
        components=Interaction()
            .add_interaction(
                Interaction()
                    .add_button(label = "Vue", style = Style.GREEN, id = "vue")
            )
    )

    # 7.
    await channel.send(
        "N*6 : Olivier C. [BDE - EPTV - VJN]#9175\nCrêpe sucre -> 3",
        components=Interaction()
            .add_button(label = "Livrer", style = Style.GREEN, id = "livrer")
    )

    # 8.
    await channel.send(
        "N*6 : Olivier C. [BDE - EPTV - VJN]#9175 Crêpe sucre -> 3 20/05/2022 17:43",
    )

class CommandCommandVJN:

    additional_function = {
        TokenType.TOKEN_REFRESH.name : refresh,
        TokenType.TOKEN_EXAMPLE.name : example,
        # TokenType.TOKEN_WORD.name : none,
    }
