'''
PDFGenerator
epubgenerator.fablepage.py

@author: Alessio Saltarin
'''

import os
import zipfile
import sys

import generators.textformatter as textformatter

class EPubFableDoc(textformatter.TextFormatter):
    
    def __init__(self, fabletitle, standalone):
        self._story = []
        pass
    
    def addCover(self, coverImageFile):
        pass
    
    def getImageFromText(self, imageTextDescription, loader):
        pass
    
    def addTitle(self, text):
        pass
    
    def addChapterTitle(self, chapter_title):
        pass
    
    def addPageBreak(self):
        pass
    
    def addParagraphOrImage(self, text, loader):
        pass
    
    def build(self):
        pass
    
    def save(self, temp_efiles_dir, epub_fullname):
        print ' - Writing ePub file...'
        try:
            self.zip_files(temp_efiles_dir, epub_fullname)
        except:
            print "***Unexpected error:", sys.exc_info()[0]
        print ' - Done.'
    
    def zip_files(self, epubdir, zip_file):
        os.chdir(epubdir)
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
                        fzip.write(fpath, compress_type=zipfile.ZIP_DEFLATED)
                        print ' - Adding '+fpath
        os.chdir('..')
    
    