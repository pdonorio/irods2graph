#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Other methods in my package
"""

import string, random
DEFAULT_PREFIX = 'abc_'

################################
## UTILITIES

def string_generator(size=32, \
    chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
    """ Create a random string of fixed size """

    # Some chaos to order
    return ''.join(random.choice(chars) for _ in range(size))

# def get_classes_from_module(mod):
#     return dict([(name, cls) \
#         for name, cls in mod.__dict__.items() if isinstance(cls, type)])

################################
## POPOLAE
# Create mock files and save them into irods
def fill_irods_random(com, icom, \
    elements=10, prefix=DEFAULT_PREFIX, tmp_dir='itmp', irods_dir='irods2graph'):

    # Clean host data
    com.remove_directory(tmp_dir, ignore=True)
    com.create_directory(tmp_dir)

    # Clean if existing on iRODS
    status = icom.check(irods_dir)

    if status == 0:
        print("Cleaning on server")
        icom.remove_directory(irods_dir)

    icom.create_directory(irods_dir)
    print("Created directory")


    # Create and save
    for i in range(1,elements):
        # Create two strings
        r1 = string_generator()
        r2 = string_generator()
        r3 = string_generator()

        # Write a random file
        filename = prefix + r1 + ".txt"
        hostfile = tmp_dir + "/" + filename
        with open(hostfile,'w') as f:
            f.write(r2)
        # Put into irods
        irods_file = irods_dir + "/" + filename
        icom.save(hostfile, irods_file)

        # Add random meta via imeta
        icom.meta_write(irods_file, [r3], [r2])
        # Debug
        #print(icom.meta_list(irods_file))

    print("Generated", elements, "elements")

    # DEBUG: Check data
    print(icom.search(prefix))

################################
## From iRODS to neo4j graph

def fill_graph_from_irods(icom, graph, elements=20, prefix=DEFAULT_PREFIX):

    data_objs = icom.search(prefix)

    for ifile in data_objs:
        ifile_metas = icom.meta_list(ifile)
        print("File:\t", ifile, "\nMetadata:\t", ifile_metas)

        dataobj = graph.DataObject(path="a",filename="b",location="c").save()

        # Graph
        #graph.save_data([])
        # Save nodes and relations

        # DEBUG - remove me!!!
        break
