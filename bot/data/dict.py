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

    def __getitem__(self, item):
        print("Coucou5")

    def __len__(self):
        return len(self.rows)
