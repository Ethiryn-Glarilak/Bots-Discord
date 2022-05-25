import re
import psycopg
from bot.data.dict import Dict

class DataBase:

    def __init__(self, host = "localhost", dbname = "discord", port = 5432, user = "bot_discord", password =  "bot"):
        self.host = host
        self.dbname = dbname
        self.port = port
        self.user = user
        self.password = password
        self.save_auto = True
        self.connect = False
        self.value = Dict()
        self.number = 2
        self.count = 0
        self.connect = self.start()

    def start(self) -> bool:
        if not self.connect:
            try:
                self.connection = psycopg.connect(
                    host = self.host,
                    dbname = self.dbname,
                    port = self.port,
                    user = self.user,
                    password = self.password,
                )
                self.cursor = self.connection.cursor()
                return True
            except psycopg.Error:
                print("Error")
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
