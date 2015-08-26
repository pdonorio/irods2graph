#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Class for neo4j database operations
"""

from py2neo import Graph, Node, Relationship

host = 'neo'
port = '7474'
# username and pw default

# Connection
graph_link = "http://neo4j:neo4j@" + host + ":" + port + "/db/data"
remote_graph = Graph(graph_link)

# Test connection
alice = Node("Person", name="Alice")
bob = Node("Person", name="Bob")
alice_knows_bob = Relationship(alice, "KNOWS", bob)
remote_graph.create(alice_knows_bob)
