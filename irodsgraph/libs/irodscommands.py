#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
My irods client class wrapper
"""

import os, inspect
from libs.bash import BashCommands
from libs import IRODS_ENV

# # All my irods command
# ICOM = {}
# ICOM["list"] = shell_commands["ils"]
# ICOM["search"] = shell_commands["ilocate"]
# ICOM["create_dir"] = shell_commands["imkdir"]
# ICOM["save"] = shell_commands["iput"]
# ICOM["remove"] = shell_commands["irm"]

class ICommands(BashCommands):
    """irods icommands in a class"""

    _init_data = {}

    def __init__(self, irodsenv=IRODS_ENV):

        # Recover plumbum shell enviroment
        super(ICommands, self).__init__()

        self.irodsenv = irodsenv
        self.iinit()
        print("iRODS environment found: ", self._init_data)

    ###################
    # ABOUT CONFIGURATION

    def iinit(self):
        """ Recover current user setup for irods """
        # Check if irods client exists and is configured
        if not os.path.exists(self.irodsenv):
            raise EnvironmentError("No irods environment found")
        #print("Found data in " + self.irodsenv)

        # Recover irods data
        data = {}
        for element in [line.strip() for line in open(self.irodsenv, 'r')]:
            key, value = element.split(" ")
            data[key] = value
        if data.__len__() < 2:
            raise EnvironmentError("Wrong irods environment: " + self.irodsenv)

        self._init_data = data
        return data

    def get_init(self):
        return self._init_data


    ###################
    # ICOMs
    def create_empty(self, path, directory=False):
        print("NOT IMPLEMENTED YET:", inspect.currentframe().f_code.co_name)
        # com = ""
        # self.execute_command(com, [path])

    def remove(self, path, recursive=False, force=False):
        com = 'irm'
        args = []
        if force:
            args.append('-f')
        if recursive:
            args.append('-r')
        args.append(path)
        # Execute
        self.execute_command(com, args)
        # Debug
        print("Removed irods object:\t", path)

    def create_directory(self, directory):
        print("NOT IMPLEMENTED YET:", inspect.currentframe().f_code.co_name)

    def list(self, path, retcodes=(0,4)):
        com = "ils"
        status = self.execute_command_advanced(com, path, retcodes=retcodes)
        return status

################################
## CONNECT TO IRODS ?
# def irods_connection(data):

#     # PROBLEM! requires PYTHON 2
#     from irods.session import iRODSSession
#     sess = iRODSSession(host='localhost', port=1247, user='rods', \
#         password='rods', zone='tempZone')