from enum import Enum
import os

import logging
__logger = logging.getLogger(__name__)

__root = os.path.dirname(__file__)


class Document(Enum):
    help = "help.txt"
    about = "about.txt"


def get_doc(document):
    assert isinstance(document, Document)
    __logger.info("Reading file {}".format(document.value))
    file_path = os.path.join(__root, document.value)
    file = open(file_path)
    content = file.read()
    file.close()
    return content
