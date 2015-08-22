#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Moving data from iRODS server to a Neo4j graphdb.

// TODO: write a irods commands class
    - be sure the class context works with click library -
    http://click.pocoo.org/5/commands/#nested-handling-and-contexts
// TOFIX: python3 irods client?

"""

import libs.cliinterface as shell_app

# MAIN
if __name__ == '__main__':
    shell_app.cli()
