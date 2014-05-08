'''
PDFGenerator
main.py

@author: Alessio Saltarin
'''

import generators.loaderfactory as loaderfactory
import character as character
import os
import sys
import time

def validate_args(fid, ebook_format, lang, sex, name, birthdate):
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
    elif (ebook_format != 'EPUB' and ebook_format != 'PDF'):
        print 'Invalid format. It must be either PDF or EPUB'
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

  pdfgenerator [fable_id] [format: PDF or EPUB] [language: EN, IT or RO] [sex: M or F] [name of the character] [birthdate]
  
  Fable IDs:
      0 - When I met the Pirates
      1 - My voyage to Aragon
      2 - The talisman of the Badia

Examples:

  - pdfgenerator 1 PDF EN F Anna 30-nov-04
  - pdfgenerator 2 EPUB IT M Andrea 26-aug-02
        
        """
    sys.exit(0)
    
if __name__ == '__main__':
    
    print """
PDF Generator v.0.990
(C) 2013-2014 FableMe.com
    """
    
    if len(sys.argv) != 7:
        help_me()

    fable_id = sys.argv[1]
    ebook_format = sys.argv[2]
    tlang = sys.argv[3]
    tsex = sys.argv[4]
    tname = sys.argv[5]
    tbirth = sys.argv[6]
    
    if (validate_args(fable_id, ebook_format, tlang, tsex, tname, tbirth)):
        print '-- Running in %s' % os.getcwd()
        print '-- Generating Fable #%s...' % fable_id
        character = character.GeneratorCharacter(tname, tsex, tbirth)
        fabledoc = loaderfactory.LoaderFactory(ebook_format, fable_id, tlang, character, False)
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
    else:
        print
        print 'Bye.'
    