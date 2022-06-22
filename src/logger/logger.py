import logging
import typing
import pathlib

class Logger(logging.Logger):

    def set_handler(self, handler):
        handler.setFormatter(logging.Formatter("%(asctime)s - %(name)-8s - %(levelname)-8s - %(message)s"))
        self.addHandler(handler)

    def set_logger(self, filename : typing.Union[str, pathlib.Path] = pathlib.Path("default.log")):
        pathlib.Path("data/log").mkdir(parents=True, exist_ok=True)
        filename = pathlib.Path("data/log").joinpath(filename)
        if filename.suffix != ".log":
            filename = filename.with_suffix(".log")
        self.set_handler(logging.FileHandler(filename))
        return self

    def add_stdout(self):
        self.set_handler(logging.StreamHandler())

class Manager(logging.Manager):

    def __init__(self):
        super().__init__(logging.Logger.root)
        self.setLoggerClass(Logger)

    def set_level(self, level : int = logging.NOTSET):
        self.level = level
        return self

    def exist_logger(self, name : str) -> bool:
        return name in self.loggerDict

    def get_logger(self, name : str, filename : typing.Union[str, pathlib.Path] = pathlib.Path("default.log"), stdout : bool = False) -> Logger:
        exist = name in self.loggerDict
        logger = self.getLogger(name)
        logger.setLevel(getattr(self, "level", 20))
        if not exist:
            logger.set_logger(filename)
            if stdout:
                logger.add_stdout()
        return logger
