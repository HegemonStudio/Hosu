import logging
import sys

from colorama import init, Fore, Style

# Initializes colorama (on Windows enables ANSI codes)
init(autoreset=True)

LEVEL_COLORS = {
    logging.DEBUG: Fore.LIGHTBLACK_EX,
    logging.INFO: Fore.BLUE,
    logging.WARNING: Fore.YELLOW,
    logging.ERROR: Fore.LIGHTRED_EX,
    logging.CRITICAL: Fore.LIGHTMAGENTA_EX,
}


class ColoredFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        color = LEVEL_COLORS.get(record.levelno, "")
        message = super().format(record)
        return f"{color}{message}{Style.RESET_ALL}"


def get_logger(name: str) -> logging.Logger:
    """
    Creates (or returns existing) logger with a standard stream handler.

    :param name: Name of the logger

    :return: Configured logger instance.
    """
    logger = logging.getLogger(name)

    # Prevent duplicate if the get_logger is called multiple times
    if logger.handlers:
        return logger

    # Create handler for logger
    handler = logging.StreamHandler(sys.stdout)
    formatter = ColoredFormatter(
        fmt="[%(asctime)s] [%(levelname)8s] [%(name)s] %(message)s",
        datefmt="%H:%M:%S",
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    logger.setLevel(logging.INFO)

    return logger
