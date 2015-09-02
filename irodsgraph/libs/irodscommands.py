#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
My irods client class wrapper.

Since python3 is not ready for API or client,
i base this wrapper on plumbum package handling shell commands.
"""

import os, inspect, re, hashlib
from libs.bash import BashCommands
from libs.templating import Templa
from libs import IRODS_ENV, TESTING

#######################################
## basic irods

class ICommands(BashCommands):
    """irods icommands in a class"""

    _init_data = {}
    _base_dir = ''

    def __init__(self, irodsenv=IRODS_ENV):

        # Recover plumbum shell enviroment
        super(ICommands, self).__init__()

        self.irodsenv = irodsenv
        self.iinit()
        print("iRODS environment found: ", self._init_data)

        self._base_dir = self.get_base_dir()

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

    def get_base_dir(self):
        com = "ipwd"
        return self.execute_command(com).strip()

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

    def current_location(self, ifile):
        """
        irods://130.186.13.14:1247/cinecaDMPZone/home/pdonorio/replica/test2
        """
        protocol = 'irods://'
        URL = protocol + \
            self._init_data['irodsHost'] +':'+ self._init_data['irodsPort'] + \
            os.path.join(self._base_dir, ifile)
        return URL

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

#######################################
## irods and metadata

class IMetaCommands(ICommands):
    """irods icommands in a class"""
    ###################
    # METADATA for irods

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

#######################################
## irods + metadata + irules
class IRuled(IMetaCommands):

    ###################
    # IRULES and templates
    def irule_execution(self, rule=None, rule_file=None):
        com='irule'
        args=[]
        if rule != None:
            args.append(rule)
        elif rule_file != None:
            args.append('-F')
            args.append(rule_file)

        # Execute
        print(com, args)
        return self.execute_command(com, args)

    def irule_from_file(self, rule_file):
        return self.irule_execution(None, rule_file)

#######################################
## EUDAT project irods configuration

class EudatICommands(IRuled):
    """ See project documentation
    http://eudat.eu/User%20Documentation%20-%20iRODS%20Deployment.html
    """

    def parse_rest_json(self, json_string=None, json_file=None):
        """ Parsing REST API output in JSON format """
        import json
        json_data = ""

        if json_string != None:
            json_data = json.loads(json_string)
        elif json_file != None:
            with open(json_file) as f:
                json_data = json.load(f)

        metas = {}
        for meta in json_data:
            key = meta['type']
            value = meta['parsed_data']
            metas[key] = value

        return metas

    # PID and replica
    def register_pid(self, dataobj):
        # Path fix
        dataobj = os.path.join(self._base_dir, dataobj)
        # Use jinja2 templating
        irule_template = "getpid"
        jin = Templa(irule_template)
        irule_file = jin.template2file({'irods_file': '"' + dataobj + '"'})
        # Call irule from template rendered
        self.irule_from_file(irule_file)
        #remove file?
        os.remove(irule_file)
        return True

    # PID and replica
    def check_pid(self, dataobj):

        if TESTING:
            # FAKE PID for testing purpose
            m = hashlib.md5(dataobj.encode('utf-8'))
            pid = m.hexdigest()
# // TO FIX: may not exists
            #pid = "842/a72976e0-5177-11e5-b479-fa163e62896a"
        else:
            print("Work in progress")
            exit()
            self.irule_from_file(irule_file)
        return pid

    def pid_metadata(self, pid):
        # Binary included inside the neoicommands docker image
        com = 'epicc'
        credentials = './cred.json'
        args = ['os', credentials, 'read', pid]

        json_data = ""
        if TESTING:
            # Fake, always the same
            pid_metas = self.parse_rest_json(None, 'out.json')
        else:
            json_data = self.execute_command(com, args).strip()
            pid_metas = self.parse_rest_json(json_data)

        # Meaningfull data
        location = pid_metas['URL']
        # e.g. irods://130.186.13.14:1247/cinecaDMPZone/home/pdonorio/replica/test2
        checksum = pid_metas['CHECKSUM']
        # e.g. sha2:dCdRWFfS2TGm/4BfKQPu1WdQSdBwxRoxCRMX3zan3SM=
        parent_pid = pid_metas['EUDAT/PPID']
        # e.g. 842/52ae4c2c-4feb-11e5-afd1-fa163e62896a

        return {
            'location': location,
            'checksum': checksum,
            'parent_pid': parent_pid
        }

################################
## CONNECT TO IRODS ?
# // TO FIX in the near future?
#     # PROBLEM! requires PYTHON 2

# def irods_connection(data):
#     from irods.session import iRODSSession
#     sess = iRODSSession(host='localhost', port=1247, user='rods', \
#         password='rods', zone='tempZone')

def do_nothing(self):
    """ Remember how to say 'not implemented yet' """
    print("NOT IMPLEMENTED YET:", inspect.currentframe().f_code.co_name)
