import logging
from ..const import *

class Formatter(logging.Formatter):
    def __init__(self, fmt: str = CLIENT_LOG_FORMAT):
        super().__init__(fmt)

    def format(self, record: logging.LogRecord) -> str:
        match record.levelno:
            case logging.DEBUG:
                record.levelname = f"\033[94m{record.levelname}\033[0m"
                record.color = ""
            case logging.INFO:
                record.levelname = f"\033[32m{record.levelname}\033[0m"
                record.color = ""
            case logging.WARNING:
                record.color = "\033[93m"
            case logging.ERROR:
                record.color = "\033[91m"
            case logging.CRITICAL:
                record.color = "\033[95m"
            case _:
                record.color = "\033[92m"
        record.reset = "\033[0m"

        return super().format(record)

def get_logger(name: str, level: int = logging.INFO, log_file: str = None): #type: ignore
    
    logger = logging.getLogger(name)
    logger.setLevel(level)

    formatter = Formatter()
    
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    if log_file:
        file_formatter = Formatter()
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    return logger