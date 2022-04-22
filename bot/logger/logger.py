import logging
import typing
import pathlib

class Logger(logging.Logger):

    def setLogger(self, filename : typing.Union[str, pathlib.Path] = pathlib.Path("default.log"), level : int = logging.NOTSET):
        filename = pathlib.Path("data/log").joinpath(filename)
        if filename.suffix != ".log":
            filename = filename.with_suffix(".log")
        handler = logging.FileHandler(filename)
        handler.setFormatter(logging.Formatter("%(asctime)s - %(name)-8s - %(levelname)-8s - %(message)s"))
        self.addHandler(handler)
        self.setLevel(level)
        return self

class Manager(logging.Manager):

    def __init__(self):
        super().__init__(logging.Logger.root)
        self.setLoggerClass(Logger)

    def setLevel(self, level : int = logging.NOTSET):
        self.level = level
        return self

    def getLogger(self, name : str, filename : typing.Union[str, pathlib.Path] = pathlib.Path("default.log")) -> Logger:
        logger = super().getLogger(name)
        logger.setLogger(filename, getattr(self, "level", 20))
        return logger
