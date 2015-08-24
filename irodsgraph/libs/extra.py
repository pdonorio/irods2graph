#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Other methods in my package
"""

import string, random
from libs.bash import BashCommands as basher
com = basher()

################################
## UTILITIES

def string_generator(size=32, \
    chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
    """ Create a random string of fixed size """

    # Some chaos to order
    return ''.join(random.choice(chars) for _ in range(size))

################################
## POPOLAE
# Create mock files and save them into irods
def fill_with_randomness(icom, \
    elements=10, prefix='abc_', \
    tmp_dir='itmp', irods_dir='mine'):

    # Clean host data
    com.remove_directory(tmp_dir, ignore=True)
    com.create_directory(tmp_dir)

    print("*** TO FIX ***")
    return

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

################################
## From iRODS to neo4j graph

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
