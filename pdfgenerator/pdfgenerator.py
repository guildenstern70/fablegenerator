'''
PDFGenerator
main.py

@author: Alessio Saltarin
'''

import pdfgenerator.loader as loader
import os
import sys

def validate_args(fid, lang, sex, name):
    validate_ok = True
    try:
        fable_id = int(fid)
    except:
        print 'Invalid fable id %s' % fid
        return False
    if (fable_id <0 or fable_id > 2):
        print 'Invalid fable id %s' % fid
        print 'Valid choices are: 0-1-2' 
        print
        validate_ok = False
    elif (lang != 'EN' and lang != 'IT' and lang != 'RO'):
        print 'Unknown lang %s' % lang
        validate_ok = False
    elif (sex != 'M' and sex != 'F'):
        print 'Invalid sex param. Valid choices are M or F.'
        validate_ok = False
    elif (name is None or len(name)<=1):
        print 'Invalid name.'
        validate_ok = False
    return validate_ok
    
if __name__ == '__main__':
    print """
PDF Generator v.0.8
(C) 2013 Alessio Saltarin
    """
    
    if len(sys.argv) != 5:
        print """        
Usage:

  python pdfgenerator.py [fable_id] [language: EN, IT or RO] [sex: M or F] [name of the character]
  
  Fable IDs:
      0 - When I met the Pirates
      1 - My voyage to Aragon
      2 - The talisman of the Badia

Example:

  python pdfgenerator.py 1 F Anna
        
        """
        sys.exit(0)
    
    fable_id = sys.argv[1]
    tlang = sys.argv[2]
    tsex = sys.argv[3]
    tname = sys.argv[4]
    
    if (validate_args(fable_id, tlang, tsex, tname)):
        print '-- Running in %s' % os.getcwd()
        print '-- Generating Fable #%s...' % fable_id
        fabledoc = loader.FableLoader(fable_id, tlang, tsex, tname)
        fabledoc.build()
        print '-- Done.'
        print '-- Saving PDF to ' + fabledoc.fable_file
        print '-- Please wait...'
        try:
            if fabledoc.save():
                print '-- PDF successfully saved'
        except IOError:
            print '** ERROR: Cannot write file. In use by another process?'
        print
        print 'All done. Bye.'
    else:
        print
        print 'Bye.'
    