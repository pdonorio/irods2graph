#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

Moving data from iRODS server to a Neo4j graphdb.

// DONE:
    * packaging, libraries and class style
    * docker section
    * iclient bootstrap script
// DOING:
    * write graphdb class and OGM models
    * entities list
// TODO:
    * add logs class
    * rancher yaml for multi host configuration
// TOFIX in the near future:
    * switch script to ipython:
        http://click.pocoo.org/5/exceptions/#what-if-i-don-t-want-that
    * python3 irods client? or stick with plumbus?

"""

import libs.cliinterface as shell_app

# MAIN
if __name__ == '__main__':
    shell_app.cli(obj={})
