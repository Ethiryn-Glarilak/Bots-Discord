class PostgresCommandVJN:

    def __init__(self):
        self.info = None
        self.db = None

    def start(self, bot):
        if self.db is None:
            raise AttributeError("DataBase not initialized")
        self.db.execute("""CREATE TABLE IF NOT EXISTS product_VJN
                            (
                                id              SERIAL PRIMARY KEY,
                                name            VARCHAR(255) NOT NULL,
                                price           MONEY NOT NULL
                            )""")
        self.db.execute("""CREATE TABLE IF NOT EXISTS command_VJN
                            (
                                id              SERIAL PRIMARY KEY,
                                id_user         BIGINT NOT NULL,
                                id_product      INT REFERENCES product_VJN(id),
                                date            DATE NOT NULL DEFAULT CURRENT_DATE,
                                price           MONEY,
                                status          INT NOT NULL
                            )""")
        self.db.execute("""CREATE TABLE IF NOT EXISTS ingredient_VJN
                            (
                                id              SERIAL PRIMARY KEY,
                                name            VARCHAR(255) NOT NULL,
                                quantities      INT
                            )""")
        self.db.execute("""CREATE TABLE IF NOT EXISTS product_ingredient_VJN
                            (
                                id_product      INT REFERENCES product_VJN(id),
                                id_ingredient   INT REFERENCES ingredient_VJN(id)
                            )""")
        bot.vjn_object.set_start_menu(bot)
