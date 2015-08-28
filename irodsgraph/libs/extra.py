#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Other methods in my package
"""

import string, random, hashlib
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

    # Create host data
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

    # Clean host data
    com.remove_directory(tmp_dir, ignore=True)

    # DEBUG: Check data
    print(icom.search(prefix))

################################
## From iRODS to neo4j graph

def fill_graph_from_irods(icom, graph, elements=20, prefix=DEFAULT_PREFIX):

    import os
    data_objs = icom.search(prefix)

    for ifile in data_objs:
        # Get metadata
        metas = icom.meta_list(ifile)

        # Getting the three pieces from Absolute Path of data object:
        # zone, location and filename
        zone = ""
        location = ""
        (head, filename) = os.path.split(ifile)
        while head != "/":
            location = os.path.join(zone, location)
            (head, zone) = os.path.split(head)

        # Zone
        try:
            # Does this already exists?
            current_zone = graph.Zone.nodes.get(name=zone)
        except graph.Zone.DoesNotExist:
            print("Saving zone", zone)
            # Save zone if not exists
            current_zone = graph.Zone(name=zone).save()

        # Save the data object inside graph
        print(zone, location, filename, metas)
        # Simulating a PID
        m = hashlib.md5(ifile.encode('utf-8'))
        pid = m.hexdigest()
        dataobj = graph.DataObject(PID=pid, \
            filename=filename, path=ifile, location=location).save()

        # Connect the object
        dataobj.located.connect(current_zone)

        # DEBUG - remove me!!!
        tmp = icom.meta_sys_list(ifile)
        print(metas, tmp)
        break
