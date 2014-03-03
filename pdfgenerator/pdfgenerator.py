'''
PDFGenerator
main.py

@author: Alessio Saltarin
'''

import pdfgenerator.loader as loader
import character as character
import os
import sys
import time

def validate_args(fid, lang, sex, name, birthdate):
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
    elif (len(birthdate) != 9):
        print 'Invalid birthdate. Must be 9 characters, ie: 26-Aug-80'
        validate_ok = False
        
    try:
        time.strptime(birthdate, "%d-%b-%y")
    except:
        print 'Cannot parse birthdate. Invalid format? Must be dd-mmm-yy'
        validate_ok = False
        
    return validate_ok

def help_me():
    print """        
Usage:

  pdfgenerator [fable_id] [language: EN, IT or RO] [sex: M or F] [name of the character] [birthdate]
  
  Fable IDs:
      0 - When I met the Pirates
      1 - My voyage to Aragon
      2 - The talisman of the Badia

Example:

  pdfgenerator 1 EN F Anna 30-nov-04
        
        """
    sys.exit(0)
    
if __name__ == '__main__':
    
    print """
PDF Generator v.0.98
(C) 2013-2014 FableMe.com
    """
    
    if len(sys.argv) != 6:
        help_me()

    fable_id = sys.argv[1]
    tlang = sys.argv[2]
    tsex = sys.argv[3]
    tname = sys.argv[4]
    tbirth = sys.argv[5]
    
    if (validate_args(fable_id, tlang, tsex, tname, tbirth)):
        print '-- Running in %s' % os.getcwd()
        print '-- Generating Fable #%s...' % fable_id
        character = character.PdfGeneratorCharacter(tname, tsex, tbirth)
        fabledoc = loader.SimpleLoader(fable_id, tlang, character)
        fabledoc.build()
        print '-- Done.'
        print '-- Saving PDF to ' + fabledoc.fable_file
        print '-- Please wait...'
        try:
            if fabledoc.save():
                print '-- PDF successfully saved'
            else:
                print '-- ERROR in writing file.'
        except IOError:
            print '** ERROR: Cannot write file. In use by another process?'
        print
        print 'All done. Bye.'
    else:
        print
        print 'Bye.'
    