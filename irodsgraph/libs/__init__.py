#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" My package """

import os, string, random

################################
## CONFIGURATION
USER_HOME = os.environ['HOME']
CONFIG_FILE = USER_HOME + "/.irodsgraph_connections.ini"
IRODS_ENV = USER_HOME + "/.irods/.irodsEnv"

## DEVELOPMENT?
#TESTING = True
TESTING = False

###########################
# Parameters
protocol = 'http'
host = 'neo'
port = '7474'
# username and pw default
user = 'neo4j'
pw = user
# Connection http descriptor
GRAPHDB_LINK = \
    protocol + "://" + user + ":" + pw + "@" + host + ":" + port + "/db/data"
# Enable OGM models db connection via environment
os.environ["NEO4J_REST_URL"] = GRAPHDB_LINK

################################
## UTILITIES

def string_generator(size=32, \
    chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
    """ Create a random string of fixed size """
    # Some chaos to order
    return ''.join(random.choice(chars) for _ in range(size))
