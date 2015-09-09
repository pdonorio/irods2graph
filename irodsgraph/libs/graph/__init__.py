#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Instance of Graph with my current models """

from libs.graph.graph import GraphDB

###########################
# Parameters
protocol = 'http'
host = 'neo'
port = '7474'
# username and pw default
user = 'neo4j'
pw = user
# Connection http descriptor
GRAPHDB_LINK = \
    protocol + "://" + user + ":" + pw + "@" + host + ":" + port + "/db/data"

################################
## Listing classes inside a module

def get_classes_from_module(mod):
    return dict([(name, cls) \
        for name, cls in mod.__dict__.items() if isinstance(cls, type)])

def get_models(lib):
    models = []
    for key, value in get_classes_from_module(lib).items():
        #print(key, value, value.__module__)
        if lib.__name__ in value.__module__:
            models.append(value)

    return models

################################
# Saving models inside the graph class, as properties

# Enable OGM models db connection via environment
import os
os.environ["NEO4J_REST_URL"] = GRAPHDB_LINK

import libs.graph.ogmmodels
graph = GraphDB()
# # This step is automatic
graph_models = get_models(ogmmodels)
graph.load_models(graph_models)
#graph.load_models()

# We are ready now
