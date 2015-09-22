#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" My package """

import os, string, random

################################
## CONFIGURATION
USER_HOME = os.environ['HOME']
CONFIG_FILE = USER_HOME + "/.irodsgraph_connections.ini"
IRODS_ENV = USER_HOME + "/.irods/.irodsEnv"
DEFAULT_PREFIX = 'abc_'

fake_directories = [
    "mydata",
    "experiments",
    "data",
    "data/test",
    "data/prototype",
    "tmp",
    "tmp/test",
]

################################
## LOGGING
#http://docs.python-guide.org/en/latest/writing/logging/
# Set default logging handler to avoid "No handler found" warnings.
import logging
LOG_LEVEL = logging.DEBUG

try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass
logging.getLogger(__name__).addHandler(NullHandler())

FORMAT = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
logging.basicConfig(format=FORMAT) #, level=logging.INFO)

def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)
    return logger

################################
## UTILITIES

def string_generator(size=32, \
    chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
    """ Create a random string of fixed size """
    # Some chaos to order
    return ''.join(random.choice(chars) for _ in range(size))

################################
## A la flask

class AppConfigs(object):
    """"Main holder for configurations"""

    mock = True

    def __init__(self, mode=None):
        super(AppConfigs, self).__init__()
        self.set(mode)

    def set(self, mode=None):
        if mode == 'production':
            self.mock = False
        elif mode is None:
            pass
        else:
            self.mock = True

    def mocking(self):
        return self.mock

# Define instance holder
appconfig = AppConfigs()
