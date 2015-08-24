#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

Moving data from iRODS server to a Neo4j graphdb.

// DONE:
    * wrote the base for irods commands class
// DOING:
    * writing classes and methods for a real package
// TOFIX:
    * python3 irods client? or stick with plumbus?
// TODO:
    * install py2neo and write a class
    * docker section/dir for images and yaml files
// BRAINSTORMING:
    * Commands extends plumbus?
    * Irods extends Commands?

"""

import libs.cliinterface as shell_app

# MAIN
if __name__ == '__main__':
    shell_app.cli(obj={})
