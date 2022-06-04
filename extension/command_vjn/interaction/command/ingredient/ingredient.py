import discord_components
from bot.interaction.interaction import Interaction
from bot.interaction.composent.button import Style
from extension.command_vjn.interaction.default import *

def menu(id_command : int, disabled : bool):
        return Interaction()\
            .add_button(label = "Pate", id = f"ingredient-pate-{id_command}")\
            .add_button(label = "Garniture", id = f"ingredient-garniture-{id_command}")\
            .add_interaction(
                Interaction()
                    .add_button(label = "Valider", style = Style.GREEN, id = f"valider-composition-{id_command}", disabled = disabled)
    # FIXME
                    # .add_button(label = "Retour", style = Style.GREY, id = f"retour-start-{id_command}")
    # FIXME
                    # .add_button(label = "Annuler", style = Style.RED, id = f"annuler-composition-{id_command}")
            )

async def compose_ingredient(interaction : discord_components.Interaction):
    id_command = interaction.custom_id.split('-')[2]
    database = interaction.client.bot.vjn_object.database
    type_ingredient = interaction.custom_id.split('-')[1] == "pate"

    # FIXME : Contenu crêpes erronée

    # FIXME
    id_product = database.execute(f"SELECT id_product FROM command_VJN WHERE id = {id_command}").fetchall()[0, "id_product"]

    # FIXME
    database.execute(f"""
        DELETE FROM
            product_ingredient_VJN
        WHERE
            (id_product, id_ingredient) IN 
                (SELECT id_product, id_ingredient FROM product_ingredient_VJN
                    JOIN (SELECT id FROM ingredient_VJN WHERE type = {type_ingredient})
                        AS ingredient_VJN
                    ON id = id_ingredient
                    WHERE id_product = {id_product})
        """).commit()

    # FIXME
    database.execute(f"""
        INSERT INTO product_ingredient_VJN (id_product, id_ingredient) VALUES
            {"".join(f"({id_product}, {ingredient.split('-')[1]}), " for ingredient in interaction.values)[:-2]}
        """).commit()

    # FIXME
    ingredients = database.execute(f"SELECT id_ingredient FROM product_ingredient_VJN WHERE id_product = {id_product}").fetchall()["id_ingredient"]
    database.execute("SELECT * FROM ingredient_VJN").fetchall()
    price = sum(float(database[str(ingredient), "price"].replace(" €", "").replace(",", ".")) for ingredient in ingredients)

    # FIXME
    database.execute(f"""
        UPDATE command_VJN
        SET price = {price}
        WHERE id = {id_command}
    """)

    # FIXME
    database.execute(f"""
        UPDATE product_VJN
        SET price = {price}
        WHERE id = {id_product}
    """)

    # FIXME
    pate_name = database.execute(f"SELECT name FROM ingredient_VJN JOIN (SELECT id_ingredient FROM product_ingredient_VJN WHERE id_product = {id_product}) AS product_ingredient_VJN ON id_ingredient = id WHERE type = True").fetchall()["name"]
    # FIXME
    garniture_name = database.execute(f"SELECT name FROM ingredient_VJN JOIN (SELECT id_ingredient FROM product_ingredient_VJN WHERE id_product = {id_product}) AS product_ingredient_VJN ON id_ingredient = id WHERE type = False").fetchall()["name"]

    valid = len(pate_name) != 1 or not garniture_name
    msg_pate ="Pate : " + "".join(f"{name}, " for name in pate_name)[:-2]
    msg_garniture = "Garniture : " + "".join(f"{name}, " for name in garniture_name)[:-2]
    content = msg_pate + "\n" + msg_garniture + "\nPrice : " + str(price).replace(".", ",") + " €\n"

    await interaction.edit_origin(content = content, components = menu(id_command, valid))
