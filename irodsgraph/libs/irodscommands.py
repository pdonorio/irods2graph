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

    def do_nothing(self):
        print("NOT IMPLEMENTED YET:", inspect.currentframe().f_code.co_name)

    def create_empty(self, path, directory=False):
        if directory:
            com = "imkdir"
        else:
            # // TODO:
            # super call of create_tempy with file (touch)
            # icp / iput of that file
            # super call of remove for the original temporary file
            print("NOT IMPLEMENTED for a file:", \
                inspect.currentframe().f_code.co_name)
            return

        # Debug
        self.execute_command(com, [path])
        print("Created", path)
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

    def save(self, path, destination=None):
        com = 'iput'
        args = [path]
        if destination is not None:
            args.append(destination)
        # Execute
        self.execute_command(com, args)
        # Debug
        print("Saved irods object from", path)

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