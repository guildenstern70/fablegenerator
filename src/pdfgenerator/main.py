'''
PDFGenerator

@author: Alessio Saltarin
'''

import os
import fablepage

OUTPUT_DIR = "../../output/"
RESOURCES_DIR = "../../resources/"

    
def build_doc(output_file):
    fable = fablepage.FableDoc(output_file)
    fable.addTitle('My voyage to Aragon')
    fable.addChapter('1', 'On the Occasion of her Ladyship''s Sixth Birthday')
    fable.addParagraph('Once upon a time, a little princess called Anna sat at her parents'' feet, and wondered what it was all about.  Turning six, that is.  What did it mean to be six? ')
    fable.addParagraph('Well, she was about to find out everything <she_he> needed to know about being six. Right in front of <her_him> was the most strangely dressed man <she_he> had ever seen - with a big pointy hat of red, yellow and green, and funny looking shoes with bells on his toes, and he had with him a beautiful gold guitar! ')
    #fable.addImage(resource_path('picturebn.jpg'), 50, 500, width=200, height=200)
    #fable.addImage(resource_path('lg.jpg'), 50, 300, width=250, height=300)
    return fable

    
def output_path(name):
    return os.path.join(OUTPUT_DIR, name)

def resource_path(name):
    return os.path.join(RESOURCES_DIR, name)
    
if __name__ == '__main__':
    
    output_file = output_path("hello.pdf")
    print 'PDF Generator v.0.1'
    print
    print '-- Generating canvas...'
    fable = build_doc(output_file)
    print '-- Done.'
    print '-- Saving PDF...'
    try:
        fable.save()
    except IOError:
        print 'ERROR: Cannot write file to ' + output_file + '. In use by another process?'
    print '-- Done.'
    print
    print 'All done. Bye.'
    