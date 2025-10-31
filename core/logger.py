import logging
import sys


def get_logger(name: str) -> logging.Logger:
  logger = logging.getLogger(name)

  if logger.handlers:
    return logger # logger has handler

  # Create handler for logger
  handler = logging.StreamHandler(sys.stdout)
  formatter = logging.Formatter(
    fmt="[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
  )
  handler.setFormatter(formatter)
  logger.addHandler(handler)

  logger.setLevel(logging.INFO)

  return logger
