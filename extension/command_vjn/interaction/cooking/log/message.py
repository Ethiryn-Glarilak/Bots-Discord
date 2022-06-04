import discord_components
import os
from extension.command_vjn.vjn_object import Status

async def livrer(interaction : discord_components.Interaction) -> None:
    id_command = interaction.custom_id.split('-')[2]
    database = interaction.client.bot.database.get("default")
    database.execute(f"""
        UPDATE command_VJN
        SET status = {Status.FINISH.value}
        WHERE id = {id_command}
    """)
    channel = interaction.client.bot.get_channel(int(os.getenv("log"))) # channel log
    await channel.send(content = interaction.message.content)
    await interaction.message.delete()
