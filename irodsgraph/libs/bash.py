#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Centralized use of plumbum package:
Use shell commands in a pythonic way.
"""

################################
# Normal bash commands
from plumbum.cmd import touch, mkdir, rm
#from plumbum import local as shell_commands

class BashCommands(object):
    """ Wrapper for execution of commands in a bash shell """

    def __init__(self):
        super(BashCommands, self).__init__()
        print("Commands init")

    ###################
    # BASE COMMANDS
    def create_empty(self, path, directory=False):

        if not directory:
            touch(path)
        else:
            mkdir(path)
        # Debug
        print("Created", path)

    def remove(self, path, recursive=False, force=False):
        # Build parameters and arguments for this command
        args = []
        if force:
            args.append('-f')
        if recursive:
            args.append('-r')
        args.append(path)
        # Execute
        rm(args)
        # Debug
        print("Removed", path)

    ###################
    # DIRECTORIES
    def create_directory(self, directory):
        self.create_empty(directory, directory=True)

    def remove_directory(self, directory, ignore=False):
        self.remove(directory, recursive=True, force=ignore)
