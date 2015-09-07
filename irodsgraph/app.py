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
    * Replica relation, Collections, Resources
    * neo4j new docker image
// DOING:
    * neo4j backup http://stackoverflow.com/a/25569005/2114395
// TODO:
    * add logs class
    * adjust template for all rules
// TOFIX
    * show counts of irods element vs selected elements
    * irods replica concept
    * switch script to ipython:
        http://click.pocoo.org/5/exceptions/#what-if-i-don-t-want-that
    * python3 irods client? or stick with plumbus?
// NOT SO FAST:
    * Recover PID in production? http://hdl.handle.net/
    * rancher yaml for multi host configuration

"""

import libs.cliinterface as shell_app

# MAIN
if __name__ == '__main__':
    shell_app.cli(obj={})
