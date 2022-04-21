import logging
import typing
import pathlib

class Logger(logging.Logger):

    def start(self, filename : typing.Union[str, pathlib.Path] = pathlib.Path("default.log"), level : int = logging.NOTSET):
        filename = pathlib.Path("data/log").joinpath(filename)
        handler = logging.FileHandler(filename)
        handler.setFormatter(logging.Formatter("%(asctime)s - %(name)-8s - %(levelname)-8s - %(message)s"))
        self.addHandler(handler)
        self.setLevel(level)
        return self

def init_logging() -> logging.Manager:
    log = logging.Manager(logging.Logger.root)
    log.setLoggerClass(Logger)
    return log
