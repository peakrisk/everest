"""
General utilities
"""
import os
import importlib

from ripl import json2py

def load_json_from_folder(folder='.'):
    """ Recursively scan a folder for json files 

    Loads the json and yields the data one at a time.
    """
    for dirpath, dirnames, filenames in os.walk(folder):
        for filename in filenames:
            if filename.endswith('.json'):
                fullpath = os.path.join(dirpath, filename)
                with open(fullpath) as infile:
                    json_data = infile.read()
                    yield(json2py.interpret(json_data))

def get_class(path):
    """ Given a path, return the class """
    path = path.split('.')

    module_name = '.'.join(path[:-1])

    module = importlib.import_module(module_name)

    return getattr(module, path[-1])

