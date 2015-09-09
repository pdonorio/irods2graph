#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
My irods client class wrapper.

Since python3 is not ready for irods unofficial client,
i base this wrapper on plumbum package handling shell commands.
"""

import os, inspect, re, random, hashlib
from libs.bash import BashCommands
from libs.templating import Templa
from libs import IRODS_ENV, string_generator, appconfig

#######################################
## basic irods

class ICommands(BashCommands):
    """irods icommands in a class"""

    _init_data = {}
    _base_dir = ''

    first_resource = 'demoResc'
    second_resource = 'replicaResc'

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

    def get_resource_from_dataobject(self, ifile):
        """ The attribute of resource from a data object """
        details = self.list(ifile, True)
        resources = []
        for element in details:
            # 2 position is the resource in irods ils -l
            resources.append(element[2])
        return resources

    def create_empty(self, path, directory=False, ignore_existing=False):
        args = [path]
        if directory:
            com = "imkdir"
            if ignore_existing:
                args.append("-p")
        else:
            # // TODO:
            # super call of create_tempy with file (touch)
            # icp / iput of that file
            # super call of remove for the original temporary file
            print("NOT IMPLEMENTED for a file:", \
                inspect.currentframe().f_code.co_name)
            return

        # Debug
        self.execute_command(com, args)
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
        # Retcodes for this particular case, skip also error 4, no file found
        retcodes = (0,4)
        (status, stdin, stdout) = self.list(path, False, retcodes)
        print("Check", path, "with", status)
        return status == 0

    def list(self, path, detailed=False, retcodes=None):
        com = "ils"
        args = [path]
        if detailed:
            args.append("-l")
        if retcodes is not None:
            return self.execute_command_advanced(com, args, retcodes=retcodes)

        # Normal command
        stdout = self.execute_command(com, args)
        lines = stdout.splitlines()
        replicas = []
        for line in lines:
            replicas.append(re.split("\s+", line.strip()))
        return replicas

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
            exit(1)
        if out:
            return out.strip().split('\n')
        return out

    def replica(self, dataobj, replicas_num=1, resOri=None, resDest=None):
        """ Replica
        Replicate a file in iRODS to another storage resource.
        Note that replication is always within a zone.
        """

        com = "irepl"
        if not resOri is not None:
            resOri = self.first_resource
        if not resDest is not None:
            resDest = self.second_resource

        args = [dataobj]
        args.append("-P") # debug copy
        args.append("-n")
        args.append(replicas_num)
        # Ori
        args.append("-S")
        args.append(resOri)
        # Dest
        args.append("-R")
        args.append(resDest)

        return self.execute_command(com, args)

    def replica_list(self, dataobj):
        return self.get_resource_from_dataobject(dataobj)

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
        """ Listing all irods metadata """
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
        """ Listing file system metadata """
        com = "isysmeta"
        args = ['ls']
        args.append(path)
        #print("iRODS sys meta for", path)
        out = self.execute_command(com, args)
        metas = {}
        if out:
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
        if rule is not None:
            args.append(rule)
            print("Executing irule", rule)
        elif rule_file is not None:
            args.append('-F')
            args.append(rule_file)
            print("Irule execution from file", rule_file)

        # Execute
        return self.execute_command(com, args)

    def irule_from_file(self, rule_file):
        return self.irule_execution(None, rule_file)

#######################################
## EUDAT project irods configuration

class EudatICommands(IRuled):
    """ See project documentation
    http://eudat.eu/User%20Documentation%20-%20iRODS%20Deployment.html
    """

    latest_pid = None

    def search(self, path, like=True):
        """ Remove eudat possible metadata from this method """
        ifiles = super(EudatICommands, self).search(path, like)
        for ifile in ifiles:
            if '.metadata/' in ifile:
                print("Skipping", ifile)
                ifiles.remove(ifile)
        return ifiles

    def execute_rule_from_template(self, rule, context={}):
        """
        Using my template class for executing an irods rule
        from a rendered file with variables in context
        """
        jin = Templa(rule)
        # Use jinja2 templating
        irule_file = jin.template2file(context)
        # Call irule from template rendered
        out = self.irule_from_file(irule_file)
        # Remove file
        os.remove(irule_file)
        # Send response back
        return out

    def parse_rest_json(self, json_string=None, json_file=None):
        """ Parsing REST API output in JSON format """
        import json
        json_data = ""

        if json_string is not None:
            json_data = json.loads(json_string)
        elif json_file is not None:
            with open(json_file) as f:
                json_data = json.load(f)

        metas = {}
        for meta in json_data:
            key = meta['type']
            value = meta['parsed_data']
            metas[key] = value

        return metas

    # PID
    def register_pid(self, dataobj):
        """ Eudat rule for irods to register a PID to a Handle """

        # Path fix
        dataobj = os.path.join(self._base_dir, dataobj)

        if appconfig.mocking():

            #pid = "842/a72976e0-5177-11e5-b479-fa163e62896a"
            # 8 - 4 - 4 - 4 - 12
            base = "842"
            code = string_generator(8)
            code += "-" + str(random.randint(1000,9999))
            code += "-" + string_generator(4) + "-" + string_generator(4)
            code += "-" + string_generator(12)
            pid = base + "/" + code

        else:
            context = {
                'irods_file': dataobj.center(len(dataobj)+2, '"')
            }
            pid = self.execute_rule_from_template('getpid', context)

        return pid

    def meta_list(self, path, attributes=[]):
        """
        Little trick to save PID from metadata listing:
        override the original method
        """
        metas = super(EudatICommands, self).meta_list(path, attributes)
        if 'PID' in metas:
            self.latest_pid = metas['PID']
        else:
            self.latest_pid = None
        return metas

    # PID
    def check_pid(self, dataobj):
        """ Should get this value from irods metadata """

        # Solved with a trick
        pid = self.latest_pid
        # Otherwise
        #self.meta_list(dataobj, ['PID'])
        # Might also use an irods rule to seek
        #self.irule_from_file(irule_file)

        return pid

    def pid_metadata(self, pid):
        """ Metadata derived only inside an Eudat enviroment """

        # Binary included inside the neoicommands docker image
        com = 'epicc'
        credentials = './conf/credentials.json'
        args = ['os', credentials, 'read', pid]

        json_data = ""
        select = {
            'location':'URL',
            'checksum': 'CHECKSUM',
            'parent_pid':'EUDAT/PPID',
        }
        metas = {}

        if appconfig.mocking():
# // TO FIX:
            empty = ""
# Generate random
# e.g. irods://130.186.13.14:1247/cinecaDMPZone/home/pdonorio/replica/test2
# e.g. sha2:dCdRWFfS2TGm/4BfKQPu1WdQSdBwxRoxCRMX3zan3SM=
# e.g. 842/52ae4c2c-4feb-11e5-afd1-fa163e62896a
            pid_metas = {
                'URL': empty,
                'CHECKSUM': empty,
                'EUDAT/PPID': empty,
            }
# // TO REMOVE:
            # Fake, always the same
            metas = self.parse_rest_json(None, './tests/epic.pid.out')

        else:
            print("Epic client for", args)
            json_data = self.execute_command(com, args).strip()
            if json_data.strip() == 'None':
                return {}

            # Get all epic metas
            metas = self.parse_rest_json(json_data)

        ## Meaningfull data
        pid_metas = {}
        for name, selection in select.items():
            value = None
            if selection in metas:
                value = metas[selection]
            pid_metas[name] = value

        return pid_metas

    def eudat_replica(self, dataobj_ori, dataobj_dest=None, pid_register=True):
        """ Replication as Eudat B2safe """

        if dataobj_dest is None:
            dataobj_dest = dataobj_ori + ".replica"
        dataobj_ori = os.path.join(self._base_dir, dataobj_ori)
        dataobj_dest = os.path.join(self._base_dir, dataobj_dest)

        context = {
            'dataobj_source': dataobj_ori.center(len(dataobj_ori)+2, '"'),
            'dataobj_dest': dataobj_dest.center(len(dataobj_dest)+2, '"'),
            'pid_register': \
                str(pid_register).lower().center(len(str(pid_register))+2, '"'),
        }

        return self.execute_rule_from_template('replica', context)

    def eudat_find_ppid(self, dataobj):
        print("***REPLICA EUDAT LIST NOT IMPLEMENTED YET ***")
        exit()

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
