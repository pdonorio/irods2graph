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

class GraphNode(StructuredNode):
    """ Extending the base Node to add some tricks """
    def getName(self):
        return self.__class__.__name__

# /tempZone/home/rods/irods2graph/abc_XdcRNnNc36YiV6iLlArDYsL7MUcEheAs.txt
# /ZONE/PATH_LOCATION_COLLECTION/NAME

class Zone(GraphNode):
    """
    iclient:/data# ips -a
    Server: localhost
         2356 rods#tempZone  0:00:00  ips  172.17.0.9
    """
    name = StringProperty(unique_index=True)
    hosting = RelationshipFrom('DataObject', 'STORED_IN')

class DataObject(GraphNode):
    """
    iRODS data object.
    - name, path, location -
    """
    path = StringProperty(unique_index=True)
    filename = StringProperty(index=True)
    location = StringProperty(index=True)
    #age = IntegerProperty(index=True, default=0)
    located = RelationshipTo(Zone, 'STORED_IN')
    hosting = RelationshipFrom('MetaData', 'LABELING')

class MetaData(GraphNode):
    """
    iclient:/data# ips -a
    Server: localhost
         2356 rods#tempZone  0:00:00  ips  172.17.0.9
    """
    key = StringProperty(unique_index=True)
    value = StringProperty(index=True)
    associated = RelationshipTo(DataObject, 'LABELING')

################################
# Saving models inside the graph class

from libs.graph import GraphDB
graph = GraphDB()
graph.load_models([DataObject, Zone])
