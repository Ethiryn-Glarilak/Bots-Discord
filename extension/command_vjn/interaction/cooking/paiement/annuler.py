import discord_components

async def annuler_paiement(interaction : discord_components.Interaction) -> None:
    id_command = interaction.custom_id.split('-')[2]
    vjn_object = interaction.client.bot.vjn_object
    database = interaction.client.bot.vjn_object.database
    database.execute(f"""
        DELETE FROM command_VJN
        WHERE id = {id_command}
    """)
    channel = interaction.client.bot.get_channel(vjn_object.log) # channel log
    message = interaction.message.content.replace("\n", " ")
    await channel.send(content=f":x: {message or f'n°{id_command} {interaction.user}'} :x:")
    if interaction.message.channel is None:
        interaction.message.channel = await interaction.user.create_dm() if interaction.channel is None else interaction.channel
    await interaction.message.delete()
