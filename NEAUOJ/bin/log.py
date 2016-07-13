__author__ = 'Code_Cola'

import os
import time
import logging
from conf.global_config import Log_PATH

class Log:
    def __init__(self):
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                            datefmt='%Y %b %d, %a <%H:%M:%S>',
                            filename=Log_PATH)

    def error(self, message):
        logging.error(message)

    def warning(self, message):
        logging.warning(message)

    def info(self, message):
        logging.info(message)

    def debug(self, message):
        logging.debug(message)
