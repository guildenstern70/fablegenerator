"""
FableGenerator
main.py

@author: Alessio Saltarin
"""

import generators.loaderfactory as loaderfactory
import os
import sys
import configuration
import logging

VERSION = "1.05"

def run(config):
    fable_id = config.fable_id
    print '-- Running in %s' % os.getcwd()
    print '-- Generating Fable #%s...' % fable_id
    fabledoc = loaderfactory.LoaderFactory(config, False)
    fabledoc.build()
    print '-- Done.'
    print '-- Saving eBook to ' + fabledoc.fable_file
    print '-- Please wait...'
    try:
        if fabledoc.save():
            print '-- eBook successfully saved'
        else:
            print '-- ERROR in writing file.'
    except IOError:
        print '** ERROR: Cannot write file. In use by another process?'
    print
    print 'All done. Bye.'

def help_me():
    print """        
Usage:

  fablegenerator [configuration_file] 
  
  [configuration_file] = Full path to configuration file

Examples of configuration file:

  [eBook]
  fable_id: 0           ; 0,1,2,3,4,5
  format: EPUB          ; PDF or EPUB
  language: EN          ; EN, IT or RO 
  sex: M                ; M or F
  name: Pippo           ; name of the character
  birthdate: 26-aug-02  ; birthdate
  dedication: to John   ; dedication
        
        """
    
if __name__ == '__main__':
    
    print """
FableGenerator """+VERSION+"""
(C) 2013-2015 FableMe.com
    """
    
    if len(sys.argv) != 2:
        help_me()
        sys.exit(0)
        
    logging.getLogger().setLevel(logging.WARN)  
    config = configuration.Configuration()
    
    if not config.read(sys.argv[1]):
        print '** Error in configuration file'
        print 'Bye.'
        sys.exit(0)
    else:
        run(config)
