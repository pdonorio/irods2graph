#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OGM: Object-Graph mapping;
Writing models for current application to describe my graph database.

// B2SAFE entities list:
    pid, checksum, replica
    metadata?
"""

from neomodel import StructuredNode, \
    StringProperty, IntegerProperty, \
    RelationshipTo, RelationshipFrom

# class GraphNode(StructuredNode):
#     """ Extending the base Node to add some tricks """
#     def getName(self):
#         return self.__class__.__name__

class Zone(StructuredNode):
    name = StringProperty(unique_index=True)
    hosting = RelationshipFrom('DataObject', 'STORED_IN')

class DataObject(StructuredNode):
    """ iRODS data object. """
    location = StringProperty(unique_index=True)
    filename = StringProperty(index=True)
    path = StringProperty()
    PID = StringProperty(index=True)    # May not exist
    located = RelationshipTo(Zone, 'STORED_IN')
    hosting = RelationshipFrom('MetaData', 'DESCRIBED_BY')

class MetaData(StructuredNode):
    """ Any metaData stored in irods """
    key = StringProperty(index=True)
    metatype = StringProperty()
    value = StringProperty(index=True)
    associated = RelationshipTo(DataObject, 'DESCRIBED_BY')

################################
# Saving models inside the graph class

from libs.graph import GraphDB
graph = GraphDB()
graph.load_models([DataObject, Zone, MetaData])
