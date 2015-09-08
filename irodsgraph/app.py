#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

Moving data from iRODS server to a Neo4j graphdb.

// DONE:
* packaging, libraries and class style
* docker section
* write graphdb class and OGM models, with entities list
* PID and rules
* Replica relation, Collections, Resources
* eudat epic client for PID metadata
* neo4j new docker image

// DOING:
    * create notebook docker image for executing queries
    * create docker images for graph and iclient
    * use my separate git repo 'dockerizing' + git submodules
// TO DO:
    * add logs class
    * adjust template for all rules
// TO FIX
    * show counts of irods element vs selected elements
    * irods replica concept
    * switch script to ipython:
        http://click.pocoo.org/5/exceptions/#what-if-i-don-t-want-that
    * python3 irods client? or stick with plumbus?
// LATER ON:
    * Recover PID in production? http://hdl.handle.net/
    * rancher yaml for multi host configuration

"""

from libs.cliinterface import cli as shell_app

# MAIN
if __name__ == '__main__':
    shell_app(obj={})
