import discord_components
import os

async def annuler_paiement(interaction : discord_components.Interaction) -> None:
    id_command = interaction.custom_id.split('-')[2]
    database = interaction.client.bot.database.get("default")
    database.execute(f"""
        DELETE FROM command_VJN
        WHERE id = {id_command}
    """)
    channel = interaction.client.bot.get_channel(int(os.getenv("log"))) # channel log
    message = interaction.message.content.replace("\n", " ")
    await channel.send(content=f":x: {message or f'n°{id_command} {interaction.user}'} :x:")
    if interaction.message.channel is None:
        interaction.message.channel = await interaction.user.create_dm() if interaction.channel is None else interaction.channel
    await interaction.message.delete()
