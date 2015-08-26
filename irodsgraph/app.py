#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

Moving data from iRODS server to a Neo4j graphdb.

// DONE:
    * wrote the base for irods commands class
    * Irods extends Commands which loads plumbus for shell
    * metadata handling inside irods class
    * install py2neo
// DOING:
    * docker section/dir for images
    * write py2neo class
// TODO:
    * docker composer
    * add logs class
    * rancher yaml for multi host configuration
// BRAINSTORMING:
    * Prototyping?
// TOFIX in the near future:
    * python3 irods client? or stick with plumbus?
    * switch script to ipython:
        http://click.pocoo.org/5/exceptions/#what-if-i-don-t-want-that

"""

import libs.cliinterface as shell_app

# MAIN
if __name__ == '__main__':
    shell_app.cli(obj={})
