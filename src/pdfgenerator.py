'''
PDFGenerator
main.py

@author: Alessio Saltarin
'''

import pdfgenerator.loader as loader
import sys
import os.path
    
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

    if (os.path.exists(file_full_path)):
        print
        print '-- Parsing %s...' % template
        print
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
            print 'ERROR: Cannot write file. In use by another process?'
        print
        print 'All done. Bye.'
    else:
        print 'Cannot find file %s' % file_full_path
        print 'Bye.'
    