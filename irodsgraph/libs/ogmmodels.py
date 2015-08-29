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
    """
    iclient:/data# ips -a
    Server: localhost
         2356 rods#tempZone  0:00:00  ips  172.17.0.9
    """
    name = StringProperty(unique_index=True)
    hosting = RelationshipFrom('DataObject', 'STORED_IN')

class DataObject(StructuredNode):
    """
    iRODS data object.
    - name, path, location -
    """
    PID = StringProperty(unique_index=True)
    filename = StringProperty(index=True)
    location = StringProperty(index=True)
    path = StringProperty()
    #age = IntegerProperty(index=True, default=0)
    located = RelationshipTo(Zone, 'STORED_IN')
    hosting = RelationshipFrom('MetaData', 'LABELING')

class MetaData(StructuredNode):
    """ MetaData found in irods """
    key = StringProperty(unique_index=True)
    value = StringProperty(index=True)
    associated = RelationshipTo(DataObject, 'LABELING')

################################
# Saving models inside the graph class

from libs.graph import GraphDB
graph = GraphDB()
graph.load_models([DataObject, Zone, MetaData])
