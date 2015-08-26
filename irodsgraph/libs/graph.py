#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Class for neo4j database operations
"""


host = 'neo'
port = '7474'
# username and pw default

# Connection
graph_link = "http://neo4j:neo4j@" + host + ":" + port + "/db/data"

#############################################
## STANDARD
# from py2neo import Graph, Node, Relationship
# remote_graph = Graph(graph_link)

# def graph_test():

#     # Test connection
#     alice = Node("Person", name="Alice")
#     bob = Node("Person", name="Bob")
#     alice_knows_bob = Relationship(alice, "KNOWS", bob)
#     remote_graph.create(alice_knows_bob)


#############################################
## OGM
import os
os.environ["NEO4J_REST_URL"] = graph_link

from neomodel import (StructuredNode, StringProperty, IntegerProperty,
    RelationshipTo, RelationshipFrom)
from neomodel import db

class Country(StructuredNode):
    code = StringProperty(unique_index=True, required=True)

    # traverse incoming IS_FROM relation, inflate to Person objects
    inhabitant = RelationshipFrom('Person', 'IS_FROM')


class Person(StructuredNode):
    name = StringProperty(unique_index=True)
    age = IntegerProperty(index=True, default=0)

    # traverse outgoing IS_FROM relations, inflate to Country objects
    country = RelationshipTo(Country, 'IS_FROM')

#http://neomodel.readthedocs.org/en/latest/batch.html

def graph_test():

    remove_all = "MATCH (n) OPTIONAL MATCH (n)-[r]-() DELETE n,r"
    # for standalone queries
    results, meta = db.cypher_query(remove_all)

    jim = Person(name='Test', age=3)   #.save()
    # jim.delete()
    # jim.refresh() # reload properties from neo
    #jim.age = 45
    jim.save() # validation happens here
    germany = Country(code='DE').save()
    jim.country.connect(germany)

    exit()
    # jim.delete()
