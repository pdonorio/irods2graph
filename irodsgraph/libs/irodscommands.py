#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
My irods client class wrapper
"""

import os
# Use shell commands in a python way
from plumbum import local as shell_commands
from libs import IRODS_ENV

# All my irods command
ICOM = {}
ICOM["list"] = shell_commands["ils"]
ICOM["search"] = shell_commands["ilocate"]
ICOM["create_dir"] = shell_commands["imkdir"]
ICOM["save"] = shell_commands["iput"]
ICOM["remove"] = shell_commands["irm"]
# Alternative?
#from plumbum.cmd import ils

################################
## CONNECT TO IRODS ?
# def irods_connection(data):

#     # PROBLEM! requires PYTHON 2
#     from irods.session import iRODSSession
#     sess = iRODSSession(host='localhost', port=1247, user='rods', \
#         password='rods', zone='tempZone')

class ICommands(object):
    """irods icommands in a class"""

    _init_data = {}

    def __init__(self, irodsenv=IRODS_ENV):
        super(ICommands, self).__init__()

        self.irodsenv = irodsenv
        #print (self.irodsenv)
        print("Ready for some iRODS")
        self.iinit()

    def iinit(self):
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
        self._init_data = data
        return data

    def get_init(self):
        return self._init_data
