#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Class for neo4j database operations
"""

import os

from libs import get_logger
logger = get_logger(__name__)

###########################
## A graph database with class as models

class GraphDB(object):
    """ Wrapper for our neo4j-db client connection"""

    def __init__(self, clean=False):
        super(GraphDB, self).__init__()
        self.check_connection()
        if clean:
            self.clean_whole_database()
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
            logger.info("Graph is connected")
        except:
            raise EnvironmentError("Missing REST url configuration for graph")

        if debug:
            # Set debug for cipher queries
            os.environ["NEOMODEL_CYPHER_DEBUG"] = "1"

    def load_models(self, models=[]):

        # from libs.graph import ogmmodels as mymodels
        # models = get_models(mymodels)

        for model in models:
            # Save attribute inside class with the same name
            setattr(self, model.__name__, model)

    def save_data(self, data):
        """ Save data inside graph db with batch process """

        #http://neomodel.readthedocs.org/en/latest/batch.html
        import inspect, sys
        logger.critical("NOT IMPLEMENTED YET: %s" \
            % inspect.currentframe().f_code.co_name)
        sys.exit(1)

    def cipher_query(self, query):
        """ Execute normal neo4j queries """
        from neomodel import db
        try:
            results, meta = db.cypher_query(query)
        except Exception as e:
            raise ("Failed to execute Cipher Query: " + query + "\n" + str(e))
        return results

    def clean_whole_database(self):
        logger.critical("Cleaning the whole graph!")
        query = self.cipher_query("MATCH (n) OPTIONAL MATCH (n)-[r]-() DELETE n,r")
        return query

    # // TO FIX:
    def create_node_if_not_exists(self, model):
        """ UHM? """
        pass
