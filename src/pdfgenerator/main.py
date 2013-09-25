'''
PDFGenerator
main.py

@author: Alessio Saltarin
'''

import loader
    
if __name__ == '__main__':
    print 'PDF Generator v.0.1'
    print
    print '-- Generating canvas...'
    fabledoc = loader.FableLoader(filename = 'My_voyage_to_Aragon.txt', title='My voyage to Aragon')
    fabledoc.build()
    print '-- Done.'
    print '-- Saving PDF to ' + fabledoc.fable_file
    print '-- Please wait...'
    try:
        fabledoc.fable.save()
        print '-- PDF successfully saved'
    except IOError:
        print 'ERROR: Cannot write file. In use by another process?'
    print
    print 'All done. Bye.'
    