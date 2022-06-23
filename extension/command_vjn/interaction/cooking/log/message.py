import discord_components
from extension.command_vjn.vjn_object import Status

async def livrer(interaction : discord_components.Interaction) -> None:
    id_command = interaction.custom_id.split('-')[2]
    vjn_object = interaction.client.bot.vjn_object
    database = interaction.client.bot.vjn_object.database
    database.execute(f"""
        UPDATE command_VJN
        SET status = {Status.FINISH.value}
        WHERE id = {id_command}
    """)
    channel = interaction.client.bot.get_channel(vjn_object.log) # channel log
    await channel.send(content = interaction.message.content)
    await interaction.message.delete()
