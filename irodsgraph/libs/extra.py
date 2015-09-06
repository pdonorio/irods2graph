#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Other methods in my package
"""

DEFAULT_PREFIX = 'abc_'
import random, pickle
from libs import TESTING, string_generator
from libs.ogmmodels import save_node_metadata

################################
## POPOLAE
# Create mock files and save them into irods
def fill_irods_random(com, icom, elements=10, clean_irods=True, \
    prefix=DEFAULT_PREFIX, tmp_dir='itmp', irods_dir='irods2graph'):

    # Create host data
    com.remove_directory(tmp_dir, ignore=True)
    com.create_directory(tmp_dir)

    if clean_irods:
        # Clean if existing on iRODS
        if icom.check(irods_dir):
            print("Cleaning on server")
            icom.remove_directory(irods_dir)
    icom.create_directory(irods_dir)

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
        metas = {}
        metas_elements = random.randint(1,5)
        for j in range(0, metas_elements):
            # More randoms
            r3 = string_generator(j)
            metatag = random.randint(1,elements)
            # Meta key
            name = "meta-" + str(metatag) #str(r3) #to make unique?
            # Content
            value = r3 + r2
            metas[name] = value

        #######################
        ## PID
        if random.randint(0,1):
            # PID may not exists
            pid = icom.register_pid(irods_file)
            print("Obtained PID", pid)

            if TESTING:
                # Save pid inside metadata
                # Automatic if using real Eudat service
                metas["PID"] = pid

        # Write metadata
        for key, value in metas.items():
            # Could use batch insert instead
            icom.meta_write(irods_file, [key], [value])
            print("Wrote", key, "in", filename)

        #######################
        ## REPLICA

        # Random choise if replica or not
        if random.randint(0,1):
            print("Replica!")

            # Random number of replicas
            n = random.randint(1,3)

            if TESTING:
                # irods simple replica
                icom.replica(irods_file, n)
                icom.replica_list(irods_file)
            else:
#// TO FIX: more copies
                icom.eudat_replica(irods_file)
                # # Eudat
                # while n > 1:
                #     n -= 1
                #     icom.eudat_replica(irods_file)

        #exit()

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
    replicas = {}

    for ifile in data_objs:

        # Limit elements as requested
        counter += 1
        if counter > elements:
            break

        print("\nWorking with", ifile)

        ##################################
        # Getting the three pieces from Absolute Path of data object:
        # zone, absolute path and filename
        # also keeps track of collections
        zone = ""
        irods_path = ""
        collections = []
        (head, filename) = os.path.split(ifile)
        while head != "/":
            # Warning: this is not irods_path as eudat thinks of it
            irods_path = os.path.join(zone, irods_path)
            # Split into basename and dir
            (head, zone) = os.path.split(head)
            #print("tmp:", zone)
            collections.append(zone)
        # Remove the last one which is the zone
        collections.remove(zone)

        # Eudat URL
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
        # Store Resource node
        details = icom.list(ifile, True)
        resource_name = details[2]
        print(resource_name); exit()
# DEBUG

        ##################################
        # Store Data Object
        current_dobj = graph.DataObject(location=location, \
            filename=filename, path=ifile).save()
        # Connect the object
        current_dobj.located.connect(current_zone)

        ##################################
        # Store Collections
        counter = 0
        last_collection = None
        #print("Collections", collections)
        for collection in collections:
            counter += 1
# // TO FIX:
# Missing absolute path attribute
            try:
                current_collection = graph.Collection.nodes.get(name=collection)
            except graph.Collection.DoesNotExist:
                print("Saving collection", collection)
                # Save zone if not exists
                current_collection = graph.Collection(name=collection).save()

            # Link the last one to zone
            if counter == 1:
                current_dobj.belonging.connect(current_collection)

            # Link the first one to dataobject
            if counter == len(collections):
                current_collection.hosted.connect(current_zone)

            # TO DO
            # Otherwise connect to the previous?
            if last_collection is not None:
                current_collection.matrioska_from.connect(last_collection)

            last_collection = current_collection

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
        # PID
        pid = icom.check_pid(ifile)

        if pid != None:
            # Create and connect
            current_pid = graph.PID(code=pid).save()
            current_dobj.identity.connect(current_pid)

            # PID Metadata
            for key, value in icom.pid_metadata(pid).items():
                #print(key, value)
                data = {'metatype':'pid', 'key':key, 'value':value}
                save_node_metadata(graph, data, current_pid, True)

                # Update PID node with checksum property
                if key == 'checksum':
                    current_pid.checksum = value
                    current_pid.save()
## Check file integrity?

                ## Check replica relation{ppid, ror}
                if key == 'parent_pid' and value is not None and value is not '':
                    replicas[pid] = value
                    print("Added replica for", pid)

        ##################################
        # Save the data object inside graph
        print("Data Object [created]\t", location)

    # Save work in progress?
    # pickle.dump(replicas, open('objs/replicas.obj',"wb"))
    # pickle.dump(graph, open('objs/graph.obj',"wb"))
    print()

    for replica, parent in replicas.items():
        #print("Replica", replica, "of", parent)
        # Connect replicas
        findconnect_frompid(graph, replica, parent)
    print("Visited", counter-1, "elements")

############################################
def findconnect_frompid(graph, pid, ppid):
    # Get node from pid
    try:
        pid_replica = graph.PID.nodes.get(code=pid)
        dobj_replica = pid_replica.identify.get()
    except graph.PID.DoesNotExist:
        print("Couldn't find PID", pid)
        exit()

    try:
        pid_parent = graph.PID.nodes.get(code=ppid)
        dobj_parent = pid_parent.identify.get()
    except graph.PID.DoesNotExist:
        print("Couldn't find PID", ppid)
        exit()

    relation = dobj_replica.replica.connect(dobj_parent)
    relation.ppid = ppid
    # // TO FIX:
    relation.ror = relation.ppid
    print("Saved replica relation for", pid, relation.ppid)
