import json
import pathlib
import typing

import src.data.link as link
from src.composant.composant import Composant

class File:

    def __init__(self, path : typing.Union[str, pathlib.Path]) -> None:
        self.path = pathlib.Path("data").joinpath(path)
        self.data = ""

    def save(self):
        with open(self.path, 'w') as file:
            file.write(self.data)

    def read(self):
        with open(self.path, 'r') as file:
            self.data = file.read()

    def save_json(self, data : Composant):
        data_json = link.get(data.__class__).to_json(data)
        with open(self.path, 'w') as file:
            json.dump(data_json, file, indent = 4)

    def read_json(self):
        with open(self.path, 'r') as file:
            data_json : dict = json.load(file)
        return link.get(data_json.get("__type__")).from_json(data_json)
