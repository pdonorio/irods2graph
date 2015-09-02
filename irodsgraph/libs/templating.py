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
    _template_dir = '../templates'

    def __init__(self, template=None):
        super(Templa, self).__init__()

        self._environment = Environment( autoescape=False, trim_blocks=False, \
            loader=FileSystemLoader(os.path.join(PATH, self._template_dir)) )

        context = {
            'irods_file': '"test.txt"',
        }
        if template != None:
            print(self.template2file(template, context))

    def render_template(self, template_filename, context):
        """ Create a string which compiles the template variables """
        return self._environment.get_template(template_filename).render(context)

    def write_to_file(self, content, filename='temp.template.rendered', mydir='/tmp'):
        """ Quickly write a file for using rendered template """
        path = os.path.join(mydir, filename)
        with open(path, 'w') as f:
            f.write(content)

    def template2file(self, template, context):
        """ Main operation for this class """
        template += '.r'
        if os.path.exists(os.path.join(PATH, self._template_dir, template)):
            print("working")
            content = self.render_template(template, context)
            self.write_to_file(content)
            return True
        return False

# ##############################
# def example():
#     urls = ['http://example.com/1', 'http://example.com/2', 'http://example.com/3']
#     context = {
#         'urls': urls
#     }
# ##############################
