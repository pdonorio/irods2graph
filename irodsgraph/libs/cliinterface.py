#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Use 'click' library to create an interface for shell execution
"""

# Make this script a powerful command line program
import click

# Click commands grouping
@click.group()
@click.option('-v', '--verbose', count=True)
def cli(verbose):
    click.echo('Script init. Verbosity: %s' % verbose)

    # # Do we have iRODS?
    # data = check_init(IRODS_ENV, CONFIG_FILE)
    # irods_connection(data)

# Option 1. Filling data inside irods
@click.command()
@click.option('--elements', default=10, type=int, \
    help='number of elements to find and convert')
def popolae(elements):
    click.echo('COMMAND:\tFilling irods.')
    #random_files_into_irods(elements)
cli.add_command(popolae)

# Option 2. Converting data from irods to a graph
@click.command()
@click.option('--elements', default=10, type=int, \
    help='number of elements to find and convert')
def convert(elements):
    click.echo('COMMAND:\tConverting iRODS objects inside a modeled graphdb')
    #fill_graph_from_irods(elements)
cli.add_command(convert)
