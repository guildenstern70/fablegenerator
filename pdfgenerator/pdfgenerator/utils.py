""" 
 
 PdfGenerator
 
 utils.py
 
"""

import os

OUTPUT_PATH = "output/"
RESOURCES_PATH = "resources/"

def get_outpath_path(filename):
    return os.path.join(OUTPUT_PATH, filename)

def get_from_relative_resources(filename):
    return os.path.join(RESOURCES_PATH, filename)

def get_from_resources(filename):
    """ Get a file stored in RESOURCE_PATH under Google App Engine """
    filepath = get_from_relative_resources(filename)
    return get_google_app_path(filepath) 

def get_google_app_path(filepath):
    """ Return the path of a file
        inside the google appengine framework """
    # Google Only abnormpath = os.path.join(os.path.split(__file__)[0], filepath) 
    return os.path.normpath(filepath)