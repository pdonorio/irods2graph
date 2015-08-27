#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Use 'click' library to create an interface for shell execution
"""

# Make this script a powerful command line program
import click
from libs.bash import BashCommands as basher
from libs.irodscommands import ICommands
from libs.config import MyConfig
from libs.ogmmodels import graph
from libs.extra import fill_irods_random, fill_graph_from_irods

############################
# Click commands grouping
@click.group()
@click.option('--debug/--no-debug', default=False)
@click.option('-v', '--verbose', count=True)
@click.pass_context
def cli(ctx, debug, verbose):
    click.echo('Script init. Verbosity: %s' % verbose)

    # Do we have iRODS?
    icom = ICommands()
    # Make sure we have an ini file for futures callback
    configurer = MyConfig(icom)
    configurer.check()

    # Save context
    ctx.obj['VERBOSE'] = verbose
    ctx.obj['DEBUG'] = debug
    ctx.obj['icom'] = icom
    ctx.obj['conf'] = configurer
    #print(dir(ctx))

############################
# Option 1. Filling data inside irods
@click.command()
@click.option('--size', default=10, type=int, \
    help='number of elements to find and convert')
@click.pass_context
def popolae(ctx, size):
    click.echo('COMMAND:\tFilling irods.')
    com = basher()  # only needed for this option
    fill_irods_random(com, ctx.obj['icom'], size)

cli.add_command(popolae)

############################
# Option 2. Converting data from irods to a graph
@click.command()
@click.option('--elements', default=10, type=int, \
    help='number of elements to find and convert')
@click.pass_context
def convert(ctx, elements):
    click.echo('COMMAND:\tConverting iRODS objects inside a modeled graphdb')
    fill_graph_from_irods(ctx.obj['icom'], graph, elements)

cli.add_command(convert)
