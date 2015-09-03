#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Other methods in my package
"""

DEFAULT_PREFIX = 'abc_'
from libs import string_generator
from libs.ogmmodels import save_node_metadata

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

            #icom.register_pid(irods_file)

##########################
# WORK IN PROGRESS
            ## Create replica relation + ppid

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
        # Store Data Object
        current_dobj = graph.DataObject(location=location, \
            filename=filename, path=ifile).save()
        # Connect the object
        current_dobj.located.connect(current_zone)

        ##################################
        # PID
        pid = icom.check_pid(ifile)
        if pid != None:
            print("We have a PID")
            current_pid = graph.PID(code=pid).save()
            current_dobj.identity.connect(current_pid)
            # PID Metadata
            for key, value in icom.pid_metadata(pid).items():
                data = {'metatype':'pid', 'key':key, 'value':value}
                save_node_metadata(graph, data, current_pid, True)

                # Update PID node{checksum}
                if key == 'checksum':
                    current_pid.checksum = value
                    current_pid.save()

#######################
# WORK IN PROGRESS

            ## Check replica relation{ppid, ror}
            ## Check integrity?

# WORK IN PROGRESS
#######################

        ##################################
        ## Other METADATA

        # System metadata
        for key, value in icom.meta_sys_list(ifile):
            data = {'metatype':'system', 'key':key, 'value':value}
            save_node_metadata(graph, data, current_dobj)

        # normal metadata, including some Eudat/B2safe
        for key, value in icom.meta_list(ifile).items():
            data = {'metatype':'classic', 'key':key, 'value':value}
            save_node_metadata(graph, data, current_dobj)


        ##################################
        # Save the data object inside graph
        print("Data Object [created]\t", location)

        # DEBUG
        print("DEBUG exit")
        break
