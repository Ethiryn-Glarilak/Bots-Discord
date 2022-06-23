import discord_components
from src.interaction.composent.button import Style
from src.interaction.interaction import Interaction

def menu(id_command : int):
    return Interaction()\
        .add_interaction(
            Interaction()
                .add_button(label = "Valider", style = Style.GREEN, id = f"valider-assigned-{id_command}")
    # FIXME
                .add_button(label = "Modifier", style = Style.BLUE, id = f"modifier-assigned-{id_command}")
    # FIXME
                # .add_button(label = "Annuler", style = Style.RED, id = f"annuler--after_assigned-{id_command}")
        )

async def assigned(interaction : discord_components.Interaction) -> None:
    id_command, cooks = interaction.custom_id.split('-')[1:]
    database = interaction.client.bot.vjn_object.database
    database.execute(f"""
        UPDATE command_VJN
        SET status = {int(cooks)}
        WHERE id = {id_command}
    """)

    emojis = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    await interaction.edit_origin(
        content = f"{interaction.message.content} to :{emojis[int(cooks) + 1]}:",
        components = menu(id_command)
    )
