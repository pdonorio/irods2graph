#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
My irods client class wrapper
"""

import os
# Use shell commands in a python way
from plumbum import local as shell_commands
from libs import USER_HOME

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
        #print (self.irodsenv)
        print("Ready for some iRODS")
        self.get_iinit()

    def get_iinit(self):
        """ Recover current user setup for irods """
        # Check if irods client exists and is configured
        if not os.path.exists(self.irodsenv):
            raise EnvironmentError("No irods environment found")
        print("Found data in " + self.irodsenv)

        # Recover irods data
        data = {}
        for element in [line.strip() for line in open(self.irodsenv, 'r')]:
            key, value = element.split(" ")
            data[key] = value
        if data.__len__() < 2:
            raise EnvironmentError("Wrong irods environment: " + self.irodsenv)

        print("Obtained irods conf:", data)
        return data
