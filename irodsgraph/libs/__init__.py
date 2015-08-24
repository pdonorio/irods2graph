#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" My package """

################################
# CENTRALIZED USE OF PLUMBUM
# Use shell commands in a pythonic way
from plumbum.cmd import mkdir, rm
#from plumbum import local as shell_commands

################################
## CONFIGURATION
import os
USER_HOME = os.environ['HOME']

CONFIG_FILE = USER_HOME + "/.irodsgraph_connections.ini"
IRODS_ENV = USER_HOME + "/.irods/.irodsEnv"
