#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Other methods in my package
"""

DEFAULT_PREFIX = 'abc_'
import random, pickle
from libs import string_generator, appconfig
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

    print("Creating", elements, "elements")
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

            if appconfig.mocking():
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

            if appconfig.mocking():
                # irods simple replica
                icom.replica(irods_file, n)
                #icom.replica_list(irods_file)
                #exit()
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
            print("Stopping at element", counter)
            break

        print("\nWorking with", ifile)

        ##################################
        # Getting the three pieces from Absolute Path of data object:
        # zone, absolute path and filename
        # also keeps track of collections
        zone = ""
        irods_path = ""
        collections = []
        (prefix, filename) = os.path.split(ifile)
        while prefix != "/":
            oripath = prefix
            # Warning: this is not irods_path as eudat thinks of it
            irods_path = os.path.join(zone, irods_path)
            # Split into basename and dir
            (prefix, zone) = os.path.split(prefix)
            # Skip the last one, as it is a zone and not a collection
            if zone != oripath.strip('/'):
                # Save collection name (zone) and its path (prefix+zone)
                collections.append((zone, oripath))

        # Eudat URL
        location = icom.current_location(ifile)

        ##################################
        # Store Zone node
        current_zone = graph.store_or_get(graph.Zone, 'name', zone)
# // TO FIX:
#Zone.get_or_create({'name':'tempZoneZZZ'})

        ##################################
        # Store Data Object
        current_dobj = graph.DataObject(location=location, \
            filename=filename, path=ifile).save()
        # Connect the object
        current_dobj.located.connect(current_zone)
        print("Created and connected data object", filename)

        ##################################
        # Get Name and Store Resource node
        resources = icom.get_resource_from_dataobject(ifile)

        for resource_name in resources:
            print("Resource", resource_name)
            current_resource = \
                graph.store_or_get(graph.Resource, 'name', resource_name)
            # Connect resource to Zone
# // TO FIX: only if not connected already
            current_resource.hosted.connect(current_zone)
            # Connect data object to this replica resource
            current_dobj.stored.connect(current_resource)

        ##################################
        # Store Collections

        collection_counter = 0
        last_collection = None
        #print("Collections", collections)

        for collection, cpath in collections:
            collection_counter += 1
            #print("COLLECTON", collection, cpath)
            current_collection = \
                graph.store_or_get(graph.Collection, 'name', collection)
            # Absolute path attribute
            if current_collection.path is not '':
                current_collection.path = cpath
                current_collection.save()

            # Link the first one to dataobject
            if collection_counter == 1:
                current_dobj.belonging.connect(current_collection)

            # Link to zone
            #if collection_counter == len(collections):
            current_collection.hosted.connect(current_zone)

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
    # Replica
    pid_replica = graph.store_only(graph.PID, 'code', pid)
    dobj_replica = pid_replica.identify.get()
    # Original copy (parent)
    pid_parent = graph.store_only(graph.PID, 'code', ppid)
    dobj_parent = pid_parent.identify.get()
    # Relationship as neomodel
    relation = dobj_replica.replica.connect(dobj_parent)
    relation.ppid = ppid
# // TO FIX: how to find ROR?
    relation.ror = relation.ppid
    print("Saved replica relation for", pid, relation.ppid)
