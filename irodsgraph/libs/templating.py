#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Templating from jinja library

example from:
https://pythonadventures.wordpress.com/2014/02/25/jinja2-example-for-generating-a-local-file-using-a-template/
"""

import os
from jinja2 import Environment, FileSystemLoader

# Find where
PATH = os.path.dirname(os.path.abspath(__file__))

class Templa(object):
    """ Using jinja2 """

    _environment = None

    def __init__(self, template=None):
        super(Templa, self).__init__()

        self._environment = Environment( autoescape=False, trim_blocks=False, \
            loader=FileSystemLoader(os.path.join(PATH, '../templates')) )

        if template != None:
            pass
        print("TO DO")

    def render_template(self, template_filename, context):
        """ Create a string which compiles the template variables """
        return self._environment.get_template(template_filename).render(context)

    def write_to_file(self, content, filename='temp.template.rendered', dir='/tmp'):
        """ Quickly write a file for using rendered template """
        with open(filename, 'w') as f:
            f.write(content)

    def template2file(self, template, context):
        """ Main operation for this class """
        content = self.render_template(template, context)
        self.write_to_file(content)
        return True

# ##############################
# def example():
#     urls = ['http://example.com/1', 'http://example.com/2', 'http://example.com/3']
#     context = {
#         'urls': urls
#     }
# ##############################
