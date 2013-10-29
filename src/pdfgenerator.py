'''
PDFGenerator
main.py

@author: Alessio Saltarin
'''

import pdfgenerator.loader as loader
import sys
import os.path

def validate_args(template, sex, name):
    validate_ok = True
    if (not os.path.exists(file_full_path)):
        print 'File %s does not exist.' % template
        print 'Valid choices are:' 
        print '  When_I_met_the_Pirates.txt' 
        print '  The_talisman_of_the_Badia.txt' 
        print '  My_voyage_to_Aragon.txt' 
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
PDF Generator v.0.5
by Alessio Saltarin (2013)
    """
    
    if len(sys.argv) != 4:
        print """ 
        
Usage:

python pdfgenerator.py [fable_text_file] [sex: M or F] [name of the character]

Example:

python pdfgenerator.py My_voyage_to_Aragon.txt F Anna
        
        """
        sys.exit(0)
    
    template = sys.argv[1]
    tsex = sys.argv[2]
    tname = sys.argv[3]
    
    file_full_path = loader.resource_path(template)

    if (validate_args(template, tsex, tname)):
        print '-- Parsing %s...' % template
        print '-- Generating canvas...'
        fabledoc = loader.FableLoader(filename = template, sex=tsex, name = tname)
        fabledoc.build()
        print '-- Done.'
        print '-- Saving PDF to ' + fabledoc.fable_file
        print '-- Please wait...'
        try:
            fabledoc.save()
            print '-- PDF successfully saved'
        except IOError:
            print '** ERROR: Cannot write file. In use by another process?'
        print
        print 'All done. Bye.'
    else:
        print 'Bye.'
    