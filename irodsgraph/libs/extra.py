#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
TO BE FIXED - THIS FILE SHOULD BE REMOVED
"""

################################
## INIT methods
def check_init(irodsenv, configuration_file, section='irods'):
    """ Prepare an ini file for future usage """

    nosection = True
    data = {}

    # If ini file already exists, search for irods section
    if os.path.exists(configuration_file):
        Config = configparser.ConfigParser()
        Config.read(configuration_file)
        if section in Config.sections():
            nosection = False
            for key in Config.options(section):
                data[key] = Config.get(section, key)

    # Get irods data and save them only if not available yet
    if nosection:
        print("No section "+section+" found")
        data = get_irods_init(irodsenv)
        write_init(configuration_file, data, section)

    return data


def get_irods_init(irodsenv):

    # Check if irods client exists and is configured
    if not os.path.exists(irodsenv):
        raise EnvironmentError("No irods environment found")
    print("Found data in " + irodsenv)

    # Recover irods data
    data = {}
    for element in [line.strip() for line in open(irodsenv, 'r')]:
        key, value = element.split(" ")
        data[key] = value
    if data.__len__() < 2:
        raise EnvironmentError("Wrong irods environment in " + irodsenv)
    return data

def write_init(configuration_file, data, section):

    # Create the section - append mode for file, since something else may exists
    with open(configuration_file,'a') as cfgfile:
        Config = configparser.ConfigParser()
        Config.add_section(section)

        for key, value in data.items():
            Config.set(section, key, value)
        Config.write(cfgfile)
    print("Wrote ini file and its irods section")

################################
## CONNECT TO IRODS ?
def irods_connection(data):
    return

    ## PROBLEM! requires PYTHON 2
    # from irods.session import iRODSSession
    # sess = iRODSSession(host='localhost', port=1247, user='rods', \
    #     password='rods', zone='tempZone')

################################
## POPOLAE

# Some chaos to order
def string_generator(size=32, \
    chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
    """ Create a random string of fixed size """
    return ''.join(random.choice(chars) for _ in range(size))

def random_files_into_irods(elements, prefix='abc_', \
    tmp_dir='itmp', irods_dir='mine'):

    # Clean host
    rm("-rf", tmp_dir)
    mkdir("-p", tmp_dir)
    # Clean existing on iRODS
    (status, stdin, stdout) = ICOM["list"][irods_dir].run(retcode = (0,4))
    if status == 0:
        print("Cleaning everything on server")
        ICOM["remove"]["-r", irods_dir]()
    ICOM["create_dir"](irods_dir)
    print("Created directory")

    # Create random files
    for i in range(1,elements):
        rand1 = string_generator()
        rand2 = string_generator()
        filename = prefix + rand1 + ".txt"
        hostfile = tmp_dir + "/" + filename
        with open(hostfile,'w') as f:
            f.write(rand2)

        # Put into irods
        ICOM["save"][hostfile, irods_dir + "/" + filename]()

    print("Generated", elements, "elements")

    # Check data
    print(ICOM["search"](prefix + '%'))

# ################################
# ## READ LOOP

def fill_graph_from_irods(elements):
    print("test")

# # Get list
# objlist = !ils [0-9a-z]*.txt
# metas = {}

# for obj in objlist:
#     ifile = os.path.basename(obj.strip())
#     meta = !imeta ls -d {ifile}
#     metas[ifile] = meta[1]
#     #print("Element " + ifile + " with meta " + meta[1])

# print(metas)
