#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Instance of Graph with my current models """

from libs.graph.graph import GraphDB
import libs.graph.ogmmodels

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
graph = GraphDB()
graph_models = get_models(ogmmodels)
# This step is automatic
graph.load_models(graph_models)

# We are ready now
