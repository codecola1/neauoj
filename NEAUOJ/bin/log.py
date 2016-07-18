__author__ = 'Code_Cola'

import logging
from conf.global_config import Log_PATH

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt='%Y %b %d, %a <%H:%M:%S>',
    filename=Log_PATH
)
