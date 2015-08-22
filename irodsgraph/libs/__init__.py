#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" My package """

################################
## LIBS
import os, string, random
#import ConfigParser #python2
import configparser
# Use shell commands in a python way
from plumbum.cmd import mkdir, rm
#from plumbum import local as shell_commands

################################
## CONFIGURATION
CONFIG_FILE = "./connections.ini"
USER_HOME = os.environ['HOME']
