"""
puml.src
========
This package contains all necessary classes to generate a uml chart from source code and
a logger object for development reasons. 
"""

from logging import (
    getLogger,
    DEBUG,
    WARNING,
    Formatter,
    StreamHandler,
)

level = WARNING
logger = getLogger()
logger.setLevel(level)

formatter = Formatter(
    "%(asctime)s - %(levelname)s : %(message)s", datefmt="%d.%m %H:%M"
)

# logger output in terminal
console_handler = StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


from .extract_class import ClassChart
from .construct_uml import UmlChart
