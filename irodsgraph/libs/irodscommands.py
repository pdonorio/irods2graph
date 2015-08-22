#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
My irods client class wrapper
"""

from libs import USER_HOME
# Use shell commands in a python way
from plumbum import local as shell_commands

IRODS_ENV = USER_HOME + "/.irods/.irodsEnv"
# All my irods command
ICOM = {}
ICOM["list"] = shell_commands["ils"]
ICOM["search"] = shell_commands["ilocate"]
ICOM["create_dir"] = shell_commands["imkdir"]
ICOM["save"] = shell_commands["iput"]
ICOM["remove"] = shell_commands["irm"]
# Alternative?
#from plumbum.cmd import ils

class ICommands(object):
    """irods icommands in a class"""
    def __init__(self, irodsenv=IRODS_ENV):
        super(ICommands, self).__init__()
        self.irodsenv = irodsenv
        print("Ready for some iRODS")
