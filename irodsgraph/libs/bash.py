#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Centralized use of plumbum package:
http://plumbum.readthedocs.org/en/latest/index.html#
- use shell commands in a more pythonic way -
"""

class BashCommands(object):
    """ Wrapper for execution of commands in a bash shell """

    _shell = None

    def __init__(self):
        # Load my personal list of commands based on my bash environment
        from plumbum import local as myshell
        self._shell = myshell

        super(BashCommands, self).__init__()
        print("Internal shell initialized")

    def execute_command(self, command, parameters=[]):
        """ Pattern in plumbum library for executing a shell command """
        self._shell[command](parameters)

    def execute_command_advanced(self, command, parameters=[], retcodes=()):
        """ Pattern in plumbum library for executing a shell command """
        (status, stdin, stdout) = self._shell[command][parameters].run(retcode=retcodes)
        return status

    ###################
    # BASE COMMANDS
    def create_empty(self, path, directory=False):

        if not directory:
            com = "touch"
        else:
            com = "mkdir"
        # Debug
        self.execute_command(com, [path])
        print("Created", path)

    def remove(self, path, recursive=False, force=False):
        # Build parameters and arguments for this command
        com = "rm"
        args = []
        if force:
            args.append('-f')
        if recursive:
            args.append('-r')
        args.append(path)
        # Execute
        self.execute_command(com, args)
        # Debug
        print("Removed", path)

    ###################
    # DIRECTORIES
    def create_directory(self, directory):
        self.create_empty(directory, directory=True)

    def remove_directory(self, directory, ignore=False):
        self.remove(directory, recursive=True, force=ignore)
