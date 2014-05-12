'''
PDFGenerator
epubgenerator.fablepage.py

@author: Alessio Saltarin
'''

import os
import zipfile
import sys

import generators.textformatter as textformatter

EPUB_SOURCES_DIR = "resources/efiles"
EPUB_OUTPUT_DIR = "../output"
EPUB_MASTER_FILE = "index.html"

class EPubFableDoc(textformatter.TextFormatter):
    
    def __init__(self, fabletitle, standalone):
        self._story = ""
        pass
    
    def addCover(self, coverImageFile):
        print '-- EPUB addCover'
        pass
    
    def getImageFromText(self, imageTextDescription, loader):
        print '-- EPUB getImageFromText'
        pass
    
    def addTitle(self, text):
        print '-- EPUB addTitle'
        pass
    
    def addChapterTitle(self, chapter_title):
        print '-- EPUB addChapterTitle'
        pass
    
    def addPageBreak(self):
        print '-- EPUB addPageBreak'
        pass
    
    def addParagraphOrImage(self, text, loader):
        print '-- EPUB addParagraphOrImage'
        pass
    
    def build(self):
        print '-- EPUB BUILD'
        pass
    
    def save(self, epub_fullname):
        print " - Current working dir : %s" % os.getcwd()
        epub_absolute = os.path.join(os.getcwd(), epub_fullname)
        print ' - EPUB SAVE Writing ePub file: ' + epub_absolute
        os.chdir(EPUB_SOURCES_DIR)
        if self.zip_files(epub_absolute):
            print ' - ePub file created successfully.'
        os.chdir('..')
        print ' - Done.'
    
    def zip_files(self, zip_file):
        save_succeeded = True
        try:
            if os.path.isfile(EPUB_MASTER_FILE):
                if os.path.isfile(zip_file):
                    print ' - Removing existing old '+zip_file
                    os.remove(zip_file)
                with zipfile.ZipFile(zip_file, 'w') as fzip:
                    # First, add mimetype
                    for root, _, files in os.walk("."):
                        for cfile in files:
                            fpath = os.path.join(root, cfile)
                            if (fpath == ".\mimetype"):
                                fzip.write(fpath)
                                print ' - Adding '+fpath
                    
                    # Second, add all other files
                    for root, _, files in os.walk("."):
                        for cfile in files:
                            fpath = os.path.join(root, cfile)
                            if (fpath != ".\mimetype"):
                                print ' - Adding '+fpath
                                fzip.write(fpath, compress_type=zipfile.ZIP_DEFLATED)
            else:
                print 'Cannot find epub XHTML. Wrong dir?'
                save_succeeded = False
        except:
            print 'Error saving ePub Zip file'
            print "Unexpected error:", sys.exc_info()[0]
            save_succeeded = False
        return save_succeeded
            
    
    