#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Other methods in my package
"""

import string, random

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
def fill_with_randomness(com, icom, \
    elements=10, prefix='abc_', tmp_dir='itmp', irods_dir='irods2graph'):

    # Clean host data
    com.remove_directory(tmp_dir, ignore=True)
    com.create_directory(tmp_dir)

    # Clean if existing on iRODS
    status = icom.list(irods_dir)

    if status == 0:
        print("Cleaning on server")
        icom.remove_directory(irods_dir)

    icom.create_directory(irods_dir)
    print("Created directory")


    # Create and save
    for i in range(1,elements):
        # Create two strings
        rand1 = string_generator()
        rand2 = string_generator()
        # Write a random file
        filename = prefix + rand1 + ".txt"
        hostfile = tmp_dir + "/" + filename
        with open(hostfile,'w') as f:
            f.write(rand2)
        # Put into irods
        #ICOM["save"][hostfile, irods_dir + "/" + filename]()
        icom.save(hostfile, irods_dir + "/" + filename)

    print("Generated", elements, "elements")

####################################
# WORKING ON
    return

    # Check data
    print(ICOM["search"](prefix + '%'))
    print("*** TO FIX ***")
    return False
# WORKING ON
####################################

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
