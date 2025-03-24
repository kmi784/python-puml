from logging import (
    getLogger,
    DEBUG, WARNING,
    Formatter,
    StreamHandler,
    FileHandler,

)
from os.path import expanduser


def setup_logger(level=DEBUG):

    log_file = expanduser("~/Developer/projects/python-puml/puml.log")
    logger = getLogger()
    logger.setLevel(level)

    formatter = Formatter(
        "%(asctime)s - %(levelname)s : %(message)s",
        datefmt="%d.%m %H:%M")

    console_handler = StreamHandler()
    console_handler.setFormatter(formatter)

    file_handler = FileHandler(log_file)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger

logger = setup_logger()

if __name__ == "__main__":
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")