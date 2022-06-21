import discord_components
from src.interaction.interaction import Interaction
from src.interaction.composent.button import Style
from extension.command_vjn.vjn_object import VJNObject
from extension.command_vjn.interaction.default import *

def set_menu(menu : Interaction, options : list):
    if len(menu) > 25:
        menu = menu[:25]
        # FIXME: Replace by a second menu
        # raise ValueError("To many options, max options are 25")
    if not menu:
        menu.append({"label": "empty category", "value": "error"})
    for option in options:
        menu.add_option(**option)

def menu(id_command, bot, default : list[int], type_ingredient : bool, interaction):
    vjn_object : VJNObject = bot.vjn_object
    database = vjn_object.database
    json : dict[dict] = vjn_object.json

    user = interaction.user
    promotion = vjn_object.free in user.roles or bot.args.free

    # FIXME
    # get_all_product(database)
    # Récupération recette existante
    database.execute("SELECT * FROM ingredient_VJN").fetchall()

    # Création composent
    menu = [{"label": f"{database[product, 'name'].capitalize()} - {database[product, 'price'] if database[product, 'price'] != '0,00 €' and not promotion else 'Gratuit'}", "value": f"ingredient-{product}", "default": int(product) in default} for product in [str(product) for product in json.get("ingredient").values()] if int(product) in database and database[product, 'type'] == type_ingredient]

    # FIXME
    # print(max(1, min(len(menu), 25)))

    start_menu = Interaction().add_menu(id = f"menu-{'pate' if type_ingredient else 'garniture'}-{id_command}", placeholder = f"Choisissez votre {'pate' if type_ingredient else 'garniture'}", max = 1 if type_ingredient else max(1, min(len(menu), 25)))
    set_menu(start_menu, menu)
    return start_menu\
# .add_interaction(
#         Interaction()
#     # FIXME
#             # .add_button(label = "Retour", style = Style.GREY, id = f"retour--composition-{id_command}")
#     # FIXME
#             # .add_button(label = "Annuler", style = Style.RED, id = f"annuler--composition-{id_command}")
#     )

async def menu_ingredient(interaction : discord_components.Interaction):
    await interaction.defer(edit_origin = True)
    type_ingredient = interaction.custom_id.split('-')[1] == "pate"
    id_command = interaction.custom_id.split('-')[2]
    bot = interaction.client.bot
    database = bot.vjn_object.database

    # FIXME
    id_product = database.execute(f"SELECT id_product FROM command_VJN WHERE id = {id_command}").fetchall()[0, "id_product"]

    # FIXME
    database.execute(f"""
        SELECT id FROM ingredient_VJN
        JOIN (SELECT * FROM product_ingredient_VJN WHERE id_product = {id_product}) AS ingredient
        ON id = id_ingredient WHERE type = {type_ingredient}
    """).fetchall()

    selected = database["id"]

    await interaction.edit_origin(
        # FIXME
        content = "Si la pâte est déjà sélectionner il faut faire `rejeter la commande`. Désolé le bouton validé n'est pas encore créé",
        components = menu(id_command, bot, selected, type_ingredient, interaction)
    )
