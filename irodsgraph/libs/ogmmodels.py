#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OGM: Object-Graph mapping;
Writing models for current application to describe my graph database.

// b2safe entities list:
    pid, checksum, replica
"""

from neomodel import StructuredNode, \
    StringProperty, IntegerProperty, \
    RelationshipTo, RelationshipFrom

class Zone(StructuredNode):
    name = StringProperty(unique_index=True)
    country = RelationshipFrom('DataObject', 'STORED_IN')

class DataObject(StructuredNode):
    """
    iRODS data object.
    - name, path, location -
    """
    path = StringProperty(unique_index=True)
    filename = StringProperty(index=True)
    location = StringProperty(index=True)
    #age = IntegerProperty(index=True, default=0)
    located = RelationshipTo(Zone, 'STORED_IN')

################################
# Saving models inside the graph class

from libs.graph import GraphDB
graph = GraphDB()
graph.load_models([DataObject, Zone])
