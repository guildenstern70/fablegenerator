'''
PDFGenerator
epubgenerator.loader.py

@author: Alessio Saltarin
'''

import fablepage

from generators import chapter, templateloader

class EPubLoader(templateloader.TemplateLoader):
    
    def __init__(self, fable_id, lang, character):
        super(EPubLoader, self).__init__(fable_id, lang, character)
        
    def build(self):
        if self._readFile():
            if len(self.paras) > 0:
                self.fable_doc = fablepage.FableDoc(self._title, standalone=True)
                self._parseFile()
                self._addCover()
                self.fable_doc.addTitle(self._title)
                for chapter in self.chapters:
                    self._buildChapter(self.fable_doc, chapter)
            else:
                print 'CRITICAL Loader Error: empty contents.'
                raise
            self.fable_doc.build() 
        