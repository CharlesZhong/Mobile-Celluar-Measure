__author__ = 'Charles'

import os, sys
import logging

reload(sys)
sys.setdefaultencoding('utf-8')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def check_files(*argchecks):
    """ Check file args exist.
    """
    def checkout_files(func):
        def wrapper(*args, **kwargs):
            for filename in argchecks:
                if not os.path.isfile(kwargs[filename]):
                    logger.error("file: [%s] is not exist!", kwargs[filename])
                    exit()
            return func(*args, **kwargs)
        return wrapper
    return checkout_files
