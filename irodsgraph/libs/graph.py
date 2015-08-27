#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Class for neo4j database operations
"""

import os

###########################
## A graph database with class as models
from libs import GRAPHDB_LINK
from neomodel import db

class GraphDB(object):
    """ Wrapper for our neo4j-db client connection"""

    #_link = GRAPHDB_LINK

    def __init__(self):
        super(GraphDB, self).__init__()
        self.check_connection()
        self.load_models()

    def check_connection(self, debug=True):
        """
        Connection is already enabled via environment inside package _init__
        This is the only way because we have a global connection for other
        python classes inside other files
        """
        # Enable OGM connection
        try:
            os.environ["NEO4J_REST_URL"]
        except:
            raise EnvironmentError("Missing REST url configuration for graph")
        print("Graph database is connected")

        if debug:
            # Set debug for cipher queries
            os.environ["NEOMODEL_CYPHER_DEBUG"] = "1"

    def load_models(self, models=[]):

        for model in models:
            # Save attribute inside class with the same name
            setattr(self, model.__name__, model)

    def save_data(self, data):
        """ Save data inside graph db with batch process """

        # Check if load models worked
        model = 'Zone'
        if model in dir(self):
            print(getattr(self, model))

        #http://neomodel.readthedocs.org/en/latest/batch.html
        import inspect
        print("NOT IMPLEMENTED YET:", inspect.currentframe().f_code.co_name)
        pass


#     #######################
#     ## CIPHER QUERY
#     remove_all = "MATCH (n) OPTIONAL MATCH (n)-[r]-() DELETE n,r"
#     # for standalone queries
#     results, meta = db.cypher_query(remove_all)
#     #print(results, meta)

#     #######################
#     jim = Person(name='Test', age=3)   #.save()
#     # jim.delete()
#     # jim.refresh() # reload properties from neo
#     #jim.age = 45
#     jim.save() # validation happens here
#     germany = Country(code='DE').save()
#     jim.country.connect(germany)

#     exit()

#############################################
## STANDARD python library
# from py2neo import Graph, Node, Relationship
# remote_graph = Graph(graph_link)
# def graph_test():
#     # Test connection
#     alice = Node("Person", name="Alice")
#     bob = Node("Person", name="Bob")
#     alice_knows_bob = Relationship(alice, "KNOWS", bob)
#     remote_graph.create(alice_knows_bob)
