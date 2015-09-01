#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
My irods client class wrapper.

Since python3 is not ready for API or client,
i base this wrapper on plumbum package handling shell commands.
"""

import os, inspect, re
from libs.bash import BashCommands
from libs import IRODS_ENV

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
            if element == '':
                continue
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
        #print("Saved irods object from", path)

    def check(self, path, retcodes=(0,4)):
        com = "ils"
        status = self.execute_command_advanced(com, path, retcodes=retcodes)
        return status

    def list(self, path, retcodes=(0,4)):
        com = "ils"
        print("NOT IMPLEMENTED YET:", inspect.currentframe().f_code.co_name)
        # status = self.execute_command_advanced(com, path, retcodes=retcodes)
        # return status

    def search(self, path, like=True):
        com = "ilocate"
        if like:
            path += '%'
        print("iRODS search for", path)
        # Execute
        try:
            out = self.execute_command(com, path)
        except Exception:
            print("No data found. " + \
                "You may try 'popolae' command first.")
# // TO FIX
            exit(1)
        if out != None:
            return out.strip().split('\n')
        return out

    ###################
    # METADATA

    def meta_command(self, path, action='list', attributes=[], values=[]):
        com = "imeta"
        args = []

        # Base commands for imeta:
        # ls, set, rm
        # - see https://docs.irods.org/master/icommands/metadata/#imeta
        if action == "list":
            args.append("ls")
        elif action == "write":
            args.append("set")
        elif action != "":
            raise KeyError("Unknown action for metadata: " + action)
        # imeta set -d FILEPATH a b
        # imeta ls -d FILEPATH
        # imeta ls -d FILEPATH a

        # File to list metadata?
        args.append("-d") # if working with data object metadata
        args.append(path)

        if len(attributes) > 0:
            if len(values) == 0 or len(attributes) == len(values):
                for key in range(0,len(attributes)):
                    args.append(attributes[key])
                    try:
                        args.append(values[key])
                    except:
                        pass
            else:
                print("No valid attributes specified for action", action)
                print(attributes, values)

        # Execute
        return self.execute_command(com, args)

    def meta_list(self, path, attributes=[]):
        out = self.meta_command(path, 'list', attributes)

        # Parse out
        metas = {}
        pattern = re.compile("attribute:\s+(.+)")
        keys = pattern.findall(out)
        pattern = re.compile("value:\s+(.+)")
        values = pattern.findall(out)
        for j in range(0, len(keys)):
            metas[keys[j]] = values[j]

        # m1 = re.search(r"attribute:\s+(.+)", out)
        # m2 = re.search(r"value:\s+(.+)", out)
        # if m1 and m2:
        #     metas[m1.group(1)] = m2.group(1)

        return metas

    def meta_sys_list(self, path):
        #isysmeta ls
        com = "isysmeta"
        args = ['ls']
        args.append(path)
        #print("iRODS sys meta for", path)
        out = self.execute_command(com, args)
        metas = {}
        if out != None:
            pattern = re.compile("([a-z_]+):\s+([^\n]+)")
            metas = pattern.findall(out)
        return metas

    def meta_write(self, path, attributes, values):
        return self.meta_command(path, 'write', attributes, values)

    ###################
    # IRULES and templates

    def rule_execution(self, rule=None, rule_file=None):
        com='irule'
        args=[]
        if rule != None:
            args.append(rule)
        elif rule_file != None:
            args.append('-F')
            args.append(rule_file)

        print(com, args)
        print("NOT IMPLEMENTED YET:", inspect.currentframe().f_code.co_name)
        return False

    def irule_from_file(self, rule_file):
        return self.rule_execution(None, rule_file)

    ###################
    # PID and replica
    def register_pid(self, dataobj):
        irule_template = ""
    # use jinja2 templating
        print("NOT IMPLEMENTED YET:", inspect.currentframe().f_code.co_name)
        irule_file = "test"
        return self.irule_from_file(irule_file)

    ###################
    def do_nothing(self):
        """ Remember how to say 'not implemented yet' """
        print("NOT IMPLEMENTED YET:", inspect.currentframe().f_code.co_name)

################################
## CONNECT TO IRODS ?
# def irods_connection(data):

#     # PROBLEM! requires PYTHON 2
#     from irods.session import iRODSSession
#     sess = iRODSSession(host='localhost', port=1247, user='rods', \
#         password='rods', zone='tempZone')
