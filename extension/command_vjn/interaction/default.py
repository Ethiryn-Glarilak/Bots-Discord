from extension.command_vjn.vjn_object import Status

# start/message/commander
def get_command_user_status(database, user, status = Status.COMMAND):
    return database.execute(f"SELECT * FROM command_VJN WHERE id_user = {user} and status = {status.value}").fetchall()

# start/message/commander
def create_command_user(database, user, status = Status.COMMAND) -> int:
    return database.execute(f"INSERT INTO command_VJN (id_user, status) VALUES ({user}, {status}) RETURNING id").fetchall()[0, "id"]

# default/message/menu
# other/message/menu
def get_all_product(database) -> None:
    database.execute("SELECT * FROM product_VJN").fetchall()

# compose/message/compose
def insert_product(database, name : str, price : int = 0) -> int:
    return database.execute(f"INSERT INTO product_VJN (name, price) VALUES ('{name}', {price}) RETURNING id").fetchall()[0, "id"]

# compose/message/compose
def update_command_product(database, id_command : int, id_product : int) -> None:
    database.execute(f"UPDATE command_VJN SET id_product = {id_product} WHERE id = {id_command}")
