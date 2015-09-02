#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Other methods in my package
"""

DEFAULT_PREFIX = 'abc_'
import string, random, hashlib
from libs.ogmmodels import save_node_metadata

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
    for i in range(1, elements+1):

        print("\nElement n." + str(i))
        # Create two strings
        r1 = string_generator()
        r2 = string_generator()

        # Write a random file
        filename = prefix + r1 + ".txt"
        hostfile = tmp_dir + "/" + filename
        with open(hostfile,'w') as f:
            f.write(r2)
        # Put into irods
        irods_file = irods_dir + "/" + filename
        icom.save(hostfile, irods_file)

        # Add random meta via imeta
        metas_elements = random.randint(1,5)
        for j in range(0, metas_elements):
            # More randoms
            r3 = string_generator(j)
            metatag = random.randint(1,elements)
            # Meta key
            name = "meta-" + str(metatag) #str(r3) #to make unique?
            # Content
            value = r3 + r2
            #print(name, value)

            # Could use batch insert instead
            icom.meta_write(irods_file, [name], [value])
            print("Wrote", name, "in", filename)


##########################
# WORK IN PROGRESS

            #icom.register_pid(irods_file)
# REMOVED IN DEBUG

            # Random choise if replica or not,
            #   - random number of replicas
            #   - Check replica(s) integrity?
            print("Debug exit")
            break
# WORK IN PROGRESS
##########################

        # Debug
        print("Created ", metas_elements, "elements")

    # Clean host data
    com.remove_directory(tmp_dir, ignore=True)
    print("COMPLETED! Generated", elements, "elements")

    # DEBUG: Check data
    #print(icom.search(prefix))

################################
## From iRODS to neo4j graph

def fill_graph_from_irods(icom, graph, elements=20, prefix=DEFAULT_PREFIX):

    import os
    data_objs = icom.search(prefix)

    counter = 0
    for ifile in data_objs:

        # Limit elements as requested
        counter += 1
        if counter > elements:
            break
        print("Working with", ifile)

        ##################################
        # Getting the three pieces from Absolute Path of data object:
        # zone, location and filename
        zone = ""
        irods_path = ""
        (head, filename) = os.path.split(ifile)
        while head != "/":
            # Warning: this is not irods_path as eudat thinks of it
            irods_path = os.path.join(zone, irods_path)
            (head, zone) = os.path.split(head)
        location = icom.current_location(ifile)

        ##################################
        # Store Zone node
        try:
            # Does this already exists?
            current_zone = graph.Zone.nodes.get(name=zone)
        except graph.Zone.DoesNotExist:
            print("Saving zone", zone)
            # Save zone if not exists
            current_zone = graph.Zone(name=zone).save()

        ##################################
        # PID

# FAKE PID for testing purpose
        pid = "842/a72976e0-5177-11e5-b479-fa163e62896a"
        m = hashlib.md5(ifile.encode('utf-8'))
        pid = m.hexdigest()
# REAL

        ##################################
        # Store Data Object
        current_dobj = graph.DataObject(location=location, \
            filename=filename, path=ifile, PID=pid).save()
        # Connect the object
        current_dobj.located.connect(current_zone)

        ##################################
        ## METADATA

        # System metadata
        for key, value in icom.meta_sys_list(ifile):
            data = {'metatype':'system', 'key':key, 'value':value}
            save_node_metadata(graph, data, current_dobj)

        # Other metadata, including Eudat/B2safe
        metas = icom.meta_list(ifile)
        # Create metadata attributes and connect
        for key, value in metas.items():
            data = {'metatype':'classic', 'key':key, 'value':value}
            save_node_metadata(graph, data, current_dobj)

        # PID Metadata
        if pid != None:
            for key, value in icom.pid_metadata(pid).items():
                data = {'metatype':'pid', 'key':key, 'value':value}
                save_node_metadata(graph, data, current_dobj)

        ##################################
        # Save the data object inside graph
        print("CREATED ***\t[Data object]\t", filename, location)

        # # DEBUG
        # break
