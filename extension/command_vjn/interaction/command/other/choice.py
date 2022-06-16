import discord_components
from extension.command_vjn.interaction.command.quantity.message import quantity

async def choice(interaction : discord_components.Interaction):
    database = interaction.client.bot.database.get("default")
    bot = interaction.client.bot
    id_command = interaction.custom_id.split('-')[2]
    id_product = interaction.values[0].split('-')[1]

    # FIXME
    database.execute(f"SELECT price FROM product_VJN WHERE id = {id_product}").fetchall()

    # FIXME
    database.execute(f"""
        UPDATE command_VJN
        SET id_product = {id_product},
            price = '{"0,00 €" if bot.args.free else database[0, "price"]}'
        WHERE id = {id_command}
    """)

    await quantity(interaction)