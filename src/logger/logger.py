import logging
import os
import pathlib
import typing

class Logger(logging.Logger):
    def __init__(self, name: str, log_file: typing.Union[str, pathlib.Path] = "default.log"):
        super().__init__(name, level=logging.INFO)

        class ColorFormatter(logging.Formatter):
            COLORS = {
            'DEBUG': '\033[94m',    # Blue
            'INFO': '\033[92m',     # Green
            'WARNING': '\033[93m',  # Yellow
            'ERROR': '\033[91m',    # Red
            'CRITICAL': '\033[95m', # Magenta
            }
            RESET = '\033[0m'
            GRAY = '\033[90m'
            VIOLET = '\033[35m'
            WHITE = '\033[97m'

            def format(self, record):
                asctime = f"{self.GRAY}{self.formatTime(record, self.datefmt)}{self.RESET}"
                name = f"{self.VIOLET}{record.name:8s}{self.RESET}"
                level = f"{self.COLORS.get(record.levelname, self.RESET)}{record.levelname:8s}{self.RESET}"
                message = f"{self.WHITE}{record.getMessage()}{self.RESET}"
                return f"{asctime} - {name} - {level} - {message}"

        formatter = ColorFormatter('%(asctime)s - %(levelname)-8s - %(name)-8s - %(message)s')
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        self.addHandler(handler)

        log_file_str = str(log_file)
        if log_file_str and log_file_str.endswith('.log'):
            log_dir = os.path.join('data', 'log')
            os.makedirs(log_dir, exist_ok=True)
            log_path = os.path.join(log_dir, log_file_str)
            file_handler = logging.FileHandler(log_path)
            file_handler.setFormatter(formatter)
            self.addHandler(file_handler)

    def log_decorator(self, level: int = logging.INFO):
        def decorator(func):
            def wrapper(*args, **kwargs):
                self.log(level, f"Calling {func.__name__} with args: {args}, kwargs: {kwargs}")
                result = func(*args, **kwargs)
                self.log(level, f"{func.__name__} returned: {result}")
                return result
            return wrapper
        return decorator

class LoggerManager(logging.Manager):
    def __init__(self, logger_class=Logger):
        super().__init__(logging.Logger.root)
        self.loggers = {}
        self.logger_class = logger_class

    @staticmethod
    def str_to_level(level_str: str) -> int:
        level_str = level_str.upper()
        if hasattr(logging, level_str):
            return getattr(logging, level_str)
        raise ValueError(f"Invalid logging level: {level_str}")

    def set_level(self, level: int = logging.NOTSET) -> 'LoggerManager':
        self.level = level
        for logger in self.loggers.values():
            logger.setLevel(level)
        return self

    def get_logger(self, name: str, log_file: typing.Union[str, pathlib.Path] = pathlib.Path("default.log")) -> Logger:
        if name not in self.loggers:
            self.loggers[name] = self.logger_class(name, log_file)
        self.loggers[name].setLevel(getattr(self, "level", logging.INFO))
        return self.loggers[name]
