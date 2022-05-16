class Generic:

    value = 0

    @staticmethod
    def generic_str():
        Generic.value += 1
        return str(Generic.value)
