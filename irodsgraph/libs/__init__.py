#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" My package """

################################
## LIBS
import os, string, random
# Use shell commands in a python way
from plumbum.cmd import mkdir, rm
#from plumbum import local as shell_commands

################################
## CONFIGURATION
USER_HOME = os.environ['HOME']
CONFIG_FILE = USER_HOME + "/.irodsgraph_connections.ini"
IRODS_ENV = USER_HOME + "/.irods/.irodsEnv"
