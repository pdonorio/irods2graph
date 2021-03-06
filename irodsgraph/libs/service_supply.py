#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Other methods in my package
"""

from libs import get_logger
logger = get_logger(__name__)

import os, random
from libs import DEFAULT_PREFIX, string_generator, \
    appconfig, fake_directories
from libs.graph.ogmmodels import save_node_metadata

################################
## POPOLAE
# Create mock files and save them into irods
def fill_irods_random(com, icom, elements=10, clean_irods=True, \
    prefix=DEFAULT_PREFIX, tmp_dir='itmp'):

    # Remove host data temporary dir if existing
    com.remove_directory(tmp_dir, ignore=True)
    # Create host data dir
    com.create_directory(tmp_dir)

    # Clean all fake dirs if requested
    if clean_irods:
        for mydir in fake_directories:
            # Clean if existing on iRODS
            if icom.check(mydir):
                logger.warning("Cleaning on server")
                icom.remove_directory(mydir)

    logger.info("Creating %s elements" % elements)
    # Create and save
    for i in range(1, elements+1):

        # Random directory, not so random
        pos = random.randint(0,len(fake_directories)-1)
        irods_dir = fake_directories[pos]
        icom.create_directory(irods_dir)

        logger.debug("Element n. %s " % i)
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
            logger.info("Obtained PID %s" % pid)

            if appconfig.mocking():
                # Save pid inside metadata
                # Automatic if using real Eudat service
                metas["PID"] = pid

        # Write metadata
        for key, value in metas.items():
            # Could use batch insert instead
            icom.meta_write(irods_file, [key], [value])
            logger.debug("Wrote key %s inside file %s " % (key, filename))

        #######################
        ## REPLICA

        # Random choise if replica or not
        if random.randint(0,1):
            logger.debug("Generating a REPLICA!")

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
    # print("Created ", metas_elements, "elements")

    # Clean host data
    com.remove_directory(tmp_dir, ignore=True)
    logger.info("COMPLETED\nGenerated n.%s elements" % elements)

    # DEBUG: Check data
    #print(icom.search(prefix))

################################
## From iRODS to neo4j graph

def fill_graph_from_irods(icom, graph, elements=0, \
    clean_graph=False, prefix=DEFAULT_PREFIX):

    if clean_graph:
        graph.clean_whole_database()

    data_objs = icom.search(prefix)

    counter = 0
    replicas = {}

    for ifile in data_objs:

        # Limit elements as requested
        counter += 1
        if elements > 0 and counter > elements:
            logger.warning("Stopping at element %s" % counter)
            break

        logger.info("Working with %s" % ifile)

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
        logger.debug("Location: %s" % location)

        ##################################
        # Store Zone node
        current_zone = graph.Zone.get_or_create({'name': zone}).pop()

        ##################################
        # Store Data Object
        current_dobj = graph.DataObject( \
            location=location, filename=filename, path=ifile).save()
        # Connect the object
        current_dobj.located.connect(current_zone)
        logger.info("Created and connected data object %s" % filename)

        ##################################
        # Get Name and Store Resource node
        resources = icom.get_resource_from_dataobject(ifile)

        for resource_name in resources:
            logger.debug("Resource %s" % resource_name)
            current_resource = \
                graph.Resource.get_or_create({'name':resource_name}).pop()
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
            properties = {
                'path': cpath,
                'name': collection,
            }
            current_collection = \
                graph.Collection.get_or_create(properties).pop()

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

            # People/User
            if key == 'data_owner_name':
                current_user = graph.Person.get_or_create({'name':value}).pop()
                current_dobj.owned.connect(current_user)

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
                    logger.info("Adding replica for %s" % pid)

        ##################################
        # Save the data object inside graph
        logger.warning("Data Object [created]\t%s" % location)

##################################
# May come handy?
    # Save work in progress?
    #import pickle
    # pickle.dump(replicas, open('objs/replicas.obj',"wb"))
    # pickle.dump(graph, open('objs/graph.obj',"wb"))
##################################

    for replica, parent in replicas.items():
        #print("Replica", replica, "of", parent)
        # Connect replicas
        findconnect_frompid(graph, replica, parent)
    logger.info("Visited %s elements" % str(counter-1))

############################################
def findconnect_frompid(graph, pid, ppid):

    # Replica
    pid_replica = graph.PID.nodes.get(code=pid)
    dobj_replica = pid_replica.identify.get()

    # Original copy (parent)
    if appconfig.mocking():
        fake = {'name':'well', 'location':'fixed'}
        dobj_parent = graph.DataObject.get_or_create(fake).pop()
    else:
        pid_parent = graph.PID.nodes.get(code=ppid)
        dobj_parent = pid_parent.identify.get()

    # Relationship as neomodel
    relation = dobj_replica.replica.connect(dobj_parent)
    relation.ppid = ppid

# // TO FIX: how to find ROR?
    relation.ror = relation.ppid

    logger.info("Saved replica relation for %s %s" % (pid, relation.ppid))
