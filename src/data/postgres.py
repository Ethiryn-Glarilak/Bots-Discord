import psycopg
from src.data.dict import Dict

class DataBase:

    def __init__(self, bot, uri = None, **connection):
        self.uri = uri

        if bot.args.test and connection.get("host", "localhost") == "localhost":
            connection["dbname"] = "test"
        self.host = connection.get("host", "localhost")
        self.dbname = connection.get("dbname", "discord")
        self.port = connection.get("port", 5432)
        self.user = connection.get("user", "bot_discord")
        self.password = connection.get("password", "bot")
        self.save_auto = True
        self.connect = False
        self.value = Dict()
        self.number = 2
        self.count = 0
        self.connect = self.start()

    def start(self) -> bool:
        if not self.connect:
            try:
                if self.uri is None:
                    self.connection = psycopg.connect(
                        host = self.host,
                        dbname = self.dbname,
                        port = self.port,
                        user = self.user,
                        password = self.password,
                    )
                else:
                    self.connection = psycopg.connect(self.uri)
                self.cursor = self.connection.cursor()
                return True
            except psycopg.Error:
                if self.uri is None:
                    print(f"Error, database = {self.dbname}")
                else:
                    print("Error, failed to connect uri")
                return False
        return self.connect

    def __del__(self):
        if self.connect:
            if self.save_auto:
                self.connection.commit()
            self.cursor.close()
            self.connection.close()

    def execute(self, query, completion : tuple = None) -> bool:
        self.start()
        if self.connect:
            if completion is not None:
                self.cursor.execute(query, completion)
            else:
                self.cursor.execute(query)
            if self.count >= self.number:
                self.commit()
            else:
                self.count += 1
        return self

    def fetchone(self) -> bool:
        if self.connect:
            self.value.set(self.cursor.description, self.cursor.fetchone())
        return self

    def fetchall(self) -> bool:
        if self.connect:
            self.value = Dict(self.cursor.description, self.cursor.fetchall())
        return self

    def set_commit(self, number : int):
        self.number = number

    def commit(self):
        if self.connect:
            self.connection.commit()
            self.count = 0

    def __iter__(self):
        if self.value.is_empty():
            return self.cursor.__iter__()
        return self.value.__iter__()

    def __item__(self):
        if self.value.is_empty():
            return self.cursor.__item__()
        return self.value.__item__()

    def __next__(self):
        if self.value.is_empty():
            return self.cursor.__next__()
        return self.value.__next__()

    def __getitem__(self, key):
        if self.value.is_empty():
            return self.cursor.__getitem__(key)
        return self.value.__getitem__(key)

    def __len__(self):
        return self.cursor.__len__() if self.value.is_empty() else self.value.__len__()

    def __contains__(self, item):
        if self.value.is_empty():
            return self.cursor.__contains__(item)
        return self.value.__contains__(item)

    def __str__(self):
        return self.cursor.__str__() if self.value.is_empty() else self.value.__str__()

    def __repr__(self):
        return self.cursor.__repr__() if self.value.is_empty() else self.value.__repr__()
