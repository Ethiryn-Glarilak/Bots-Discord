import psycopg

class Dict:

    """Defaults id columns considered as primary key"""

    def __init__(self, columns: list[psycopg.Column] = None, rows: list[tuple] = None):
        if columns is None:
            columns = []
        if rows is None:
            rows = []
        self.rows = rows
        self.columns = columns
        self._pos = 0

    def is_empty(self):
        return len(self.columns) == 0 and len(self.rows) == 0

    def __iter__(self):
        return self

    def __item__(self):
        print("Coucou3")

    def __next__(self):
        if self._pos != len(self.rows):
            self._pos += 1
            return self.rows[self._pos - 1]
        self._pos = 0
        raise StopIteration

    def get_columns(self, columns):
        return next((index for index, column in enumerate(self.columns) if column.name == columns), 0)

    def set_rc(self, item):
        if isinstance(item[0], int) and isinstance(item[1], str):
            return item[0], self.get_columns(item[1])
        elif isinstance(item[0], int) and isinstance(item[1], int):
            return item
        elif isinstance(item[0], str) and isinstance(item[1], int):
            return item[1], self.get_columns(item[0])
        elif isinstance(item[0], str) and isinstance(item[1], str):
            return self["id"].index(int(item[0])), self.get_columns(item[1])
        else:
            raise NotImplementedError("This type getitem is not supported")

    def __getitem__(self, item):
        if isinstance(item, int):
            return self.rows[self["id"].index(str(item))]

        if isinstance(item, str):
            return [row[self.get_columns(item)] for row in self.rows]

        if not isinstance(item, tuple):
            raise NotImplementedError("This type getitem is not supported")
        rows, columns = self.set_rc(item)
        return self.rows[rows][columns]

    def __len__(self):
        return len(self.rows)

    def __contains__(self, item):
        return item in self["id"]

    def __str__(self):
        return self.rows.__str__()
