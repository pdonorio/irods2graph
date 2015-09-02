#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" My package """

################################
## TESTING PURPOSE
TESTING = True
#TESTING = False

################################
## CONFIGURATION
import os
USER_HOME = os.environ['HOME']

CONFIG_FILE = USER_HOME + "/.irodsgraph_connections.ini"
IRODS_ENV = USER_HOME + "/.irods/.irodsEnv"

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
