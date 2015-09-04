__author__ = 'Code_Cola'

import time
import logging


class Log:
    def __init__(self):
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                            datefmt='%Y %b %d, %a <%H:%M:%S>',
                            filename='web/log/web.log',)#../../web/log/

    def info(self, message):
        logging.info(message)

    def warning(self, message):
        logging.warning(message)