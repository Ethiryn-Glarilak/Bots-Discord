class Group(dict):

    counter : int = 0

    def get_name(self):
        if self.counter > 2**10:
            self.counter = 0
        else:
            self.counter += 1
        return self.counter

    def see_name(self):
        return self.counter

    def __init__(self, name : str = None, mode : int = 0, next : tuple[str, int] = None):
        """Init Group

        Args:
            name (str, optional): Name to find easily. Defaults to None.
            mode (int, optional): OR/AND/NOT. Defaults to 0.
            next (list[str, int], optional): tuple(name, mode) of next for mode == 2. Defaults to None.

        Raises:
            ValueError: If next is defined but mode is not 2.
        """
        if mode == 2:
            if next is None:
                next = []
            self.append(Group(*next))
            self.element = self.see_name()
            def append(self, add): # Pas sur que ça ait marché il faut tester
                self[-1].append(add)
        elif next is not None:
            raise ValueError("Mode next must not defined if mode is not 2.")
        self.mode = mode # 0 = OR; 1 = AND; 2 = NOT
        self.name = self.get_name() if name is None else name

    def children(self, name : str = None, mode : int = None, next : tuple[str, int] = None):
        """Create a children group

        Args:
            name (str, optional): Name to find easily. Defaults to None.
            mode (int, optional): OR/AND/NOT. Defaults to None.
            next (list[str, int], optional): tuple(name, mode) of next for mode == 2. Defaults to None.

        Returns:
            _type_: _description_
        """
        if mode is None: # Set mode at next step if not explicitly defined.
            mode = (self.mode + 1) % 2
        group = Group(mode, name, next)
        self.append(group, name)
        return group

    def append(self, value, name = None):
        if name is None:
            name = self.get_name()
        self[name] = value

    def __item__(self, name):
        if self.get(name, None) is None:
            raise ValueError("Unknown")
        return self.get(name)

    def check(self, other):
        if len(self) == 0:
            return self.mode != 2

        for element in self.values():
            if element.check(other):
                if self.mode == 0: # OR
                    return True
                elif self.mode == 1: # AND
                    continue
                elif self.mode == 2: # NOT
                    return False
            elif self.mode == 0: # OR
                continue
            elif self.mode == 1: # AND
                return False
            elif self.mode == 2: # NOT
                return True

        return self.mode == 1
