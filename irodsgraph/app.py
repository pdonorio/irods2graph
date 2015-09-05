#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

Moving data from iRODS server to a Neo4j graphdb.

// DONE:
    * packaging, libraries and class style
    * docker section
    * write graphdb class and OGM models, with entities list
    * PID and rules
    * eudat epic client for PID metadata
    * Replica relation
    * Collections
// DOING:
    * Resources
    * Skip .metadata directory!
    * add logs class
// TODO:
    * template all rules
// TOFIX
    * show counts of irods element vs selected elements
    * switch script to ipython:
        http://click.pocoo.org/5/exceptions/#what-if-i-don-t-want-that
    * python3 irods client? or stick with plumbus?
// NOT SO FAST:
    * Recover PID in production? http://hdl.handle.net/
    * Update docker neo4j https://hub.docker.com/r/neo4j/neo4j/
    * rancher yaml for multi host configuration

"""

import libs.cliinterface as shell_app

# MAIN
if __name__ == '__main__':
    shell_app.cli(obj={})
