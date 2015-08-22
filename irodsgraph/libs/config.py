#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Internal app config using ".ini" configparser
"""

import os
#import ConfigParser #python2
import configparser
from libs import CONFIG_FILE

class MyConfig(object):
    """My personal ini configuration for speeding app usage"""

    def __init__(self, icom, configuration_file=CONFIG_FILE):
        super(MyConfig, self).__init__()
        self.icom = icom
        self.conffile = configuration_file

        # // TO FIX: should i open in write mode forever?
        self.configurer = configparser.ConfigParser()

    def check_init(self, section='irods'):
        """ Prepare an ini file for future usage """

        nosection = True
        data = {}

        # If ini file already exists, search for irods section
        if os.path.exists(self.conffile):
            Config.read(self.conffile)
            if section in Config.sections():
                nosection = False
                for key in Config.options(section):
                    data[key] = Config.get(section, key)

        # Get irods data and save them only if not available yet
        if nosection:
            print("No section "+section+" found")
            data = get_irods_init(irodsenv)
            write_init(self.conffile, data, section)

        return data

    def write_init(self, data, section):

        # Create the section - append mode for file, since something else may exists
        with open(self.conffile,'a') as cfgfile:
            Config = configparser.ConfigParser()
            Config.add_section(section)

            for key, value in data.items():
                Config.set(section, key, value)
            Config.write(cfgfile)
        print("Wrote ini file and its irods section")
