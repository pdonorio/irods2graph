#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Internal app config using ".ini" configparser
"""

from libs import get_logger

import os
from libs import CONFIG_FILE
try:
    import configparser
except:
    # python2
    import ConfigParser as configparser

logger = get_logger(__name__)


class MyConfig(object):
    """My personal ini configuration for speeding app usage"""

    section = 'irods'

    def __init__(self, icom, configuration_file=CONFIG_FILE):
        super(MyConfig, self).__init__()
        self.icom = icom
        self.conffile = configuration_file

        # // TO FIX: should i open in write mode forever?
        self.configurer = configparser.ConfigParser()

    def check(self):
        """ Prepare an ini file for future usage """

        nosection = True
        data = {}

        # If ini file already exists, search for irods section
        if os.path.exists(self.conffile):
            self.configurer.read(self.conffile)
            if self.section in self.configurer.sections():
                nosection = False
                for key in self.configurer.options(self.section):
                    data[key] = self.configurer.get(self.section, key)

        # Get irods data and save them only if not available yet
        if nosection:
            logger.warning("No section %s found" % self.section)
            data = self.icom.get_init()
            self.save(data)

        return data

    def save(self, data):

        # Create the section - append mode for file, since something else may exists
        with open(self.conffile,'a') as cfgfile:
            self.configurer.add_section(self.section)

            for key, value in data.items():
                self.configurer.set(self.section, key, value)
            self.configurer.write(cfgfile)
        logger.debug("Wrote ini file and its irods section")
