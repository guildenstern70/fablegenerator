'''
PDFGenerator
epubgenerator.fablepage.py

@author: Alessio Saltarin
'''

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
    
    def save(self):
        pass
    
    