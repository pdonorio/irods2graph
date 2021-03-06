#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Use 'click' library to create an interface for shell execution
"""

from libs import get_logger
logger = get_logger(__name__)

# Make this script a powerful command line program
import click
from libs.bash import BashCommands as basher
from libs.irodscommands import EudatICommands
from libs.config import MyConfig
from libs import appconfig

############################
# Click commands grouping
@click.group()
@click.option('-v', '--verbose', count=True)
@click.option('--debug/--no-debug', default=False)
@click.option('--mock/--no-mock', default=False)
@click.pass_context
def cli(ctx, verbose, debug, mock):
    logger.debug('Script init. Verbosity: %s' % verbose)
    logger.debug('Debug: %s' % debug)
    if mock:
        appconfig.set('devel')
    else:
        appconfig.set('production')

    # Do we have iRODS?
    icom = EudatICommands()
    # Make sure we have an ini file for futures callback
    configurer = MyConfig(icom)
    configurer.check()

    # Save context
    ctx.obj['VERBOSE'] = verbose
    ctx.obj['DEBUG'] = debug
    ctx.obj['MOCK'] = mock
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
    logger.info('COMMAND: Filling irods')

    com = basher()  # system commands, only needed for this command
    remove_irods_existing = appconfig.mocking()
    from libs.service_supply import fill_irods_random
    fill_irods_random(com, ctx.obj['icom'], size, remove_irods_existing)

cli.add_command(popolae)

############################
# Option 2. Converting data from irods to a graph
@click.command()
@click.option('--elements', default=0, type=int, \
    help='number of elements to find and convert') #note: 0 is all
@click.pass_context
def convert(ctx, elements):
    logger.info('COMMAND: Converting iRODS objects inside a modeled graphdb')

    # Loading the library opens the graph connection
    from libs.graph import graph    # only needed for this command
    #remove_graph_existing = appconfig.mocking()
    remove_graph_existing = True #DEBUG
    from libs.service_supply import fill_graph_from_irods
    fill_graph_from_irods(ctx.obj['icom'], graph, elements, remove_graph_existing)

cli.add_command(convert)
