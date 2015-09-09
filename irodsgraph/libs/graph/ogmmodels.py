#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OGM: Object-Graph mapping;
Writing models for current application to describe my graph database.
"""

from neomodel import StringProperty, \
    StructuredNode, StructuredRel, \
    RelationshipTo, RelationshipFrom

################################
## MODELS

class Zone(StructuredNode):
    name = StringProperty(unique_index=True)
    # Relations
    hosting = RelationshipFrom('DataObject', 'IS_LOCATED_IN')
    hosting_res = RelationshipFrom('Resource', 'IS_AVAILABLE_IN')
    hosting_col = RelationshipFrom('Collection', 'IS_PLACED_IN')

class Resource(StructuredNode):
    name = StringProperty(unique_index=True)
    # Relations
    store = RelationshipFrom('DataObject', 'STORED_IN')
    described = RelationshipFrom('MetaData', 'DESCRIBED_BY')
    hosted = RelationshipTo(Zone, 'IS_AVAILABLE_IN')

class Collection(StructuredNode):
    """ iRODS collection of data objects [Directory] """
    path = StringProperty(unique_index=True)
    name = StringProperty()
    # Relations
    belongs = RelationshipFrom('DataObject', 'BELONGS_TO')
    described = RelationshipFrom('MetaData', 'DESCRIBED_BY')
    hosted = RelationshipTo(Zone, 'IS_PLACED_IN')
    # Also Related to itself: a collection may be inside a collection.
    matrioska_from = RelationshipFrom('Collection', 'INSIDE')
    matrioska_to = RelationshipTo('Collection', 'INSIDE')

class Replication(StructuredRel):
    """
    Replica connects a DataObject to its copies.
        Note: this is a relationship, not a node.
    """
    # Parent
    PPID = StringProperty()
    # Ancestor
    ROR = StringProperty()

class DataObject(StructuredNode):
    """ iRODS data object [File] """
    location = StringProperty(unique_index=True)
    #PID = StringProperty(index=True)    # May not exist
    filename = StringProperty(index=True)
    path = StringProperty()
    # Relations
    located = RelationshipTo(Zone, 'IS_LOCATED_IN')
    stored = RelationshipTo(Resource, 'STORED_IN')
    belonging = RelationshipTo(Collection, 'BELONGS_TO')
    replica = RelationshipTo('DataObject', 'IS_REPLICA_OF', model=Replication)
    described = RelationshipFrom('MetaData', 'DESCRIBED_BY')
    identity = RelationshipFrom('PID', 'UNIQUELY_IDENTIFIED_BY')

class PID(StructuredNode):
    """
    EUDAT Persistent Identification (PID)
    http://eudat.eu/User%20Documentation%20-%20PIDs%20in%20EUDAT.html
    """
    code = StringProperty(unique_index=True)
    checksum = StringProperty(index=True)   # For integrity
    # Relations
    described = RelationshipFrom('MetaData', 'DESCRIBED_BY')
    identify = RelationshipTo(DataObject, 'UNIQUELY_IDENTIFIED_BY')

class MetaData(StructuredNode):
    """ Any metaData stored in any service level """
    key = StringProperty(index=True)
    metatype = StringProperty()         # Describe the level of metadata
    value = StringProperty(index=True)
    # Relations
    pid = RelationshipTo(PID, 'DESCRIBED_BY')
    data = RelationshipTo(DataObject, 'DESCRIBED_BY')
    resource = RelationshipTo(Resource, 'DESCRIBED_BY')
    collection = RelationshipTo(Collection, 'DESCRIBED_BY')

################################
# Utilities functions

def save_node_metadata(graph_node, data, from_node=None, pid=False):
    """ Generic pattern of saving metadata and connecting a node """
    obj = graph_node.MetaData(**data).save()
    if from_node != None:
        if pid:
            obj.pid.connect(from_node)
        else:
            obj.data.connect(from_node)
    #print("Saved and connected", data)
