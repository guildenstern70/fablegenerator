'''
PDFGenerator
epubgenerator.loader.py

@author: Alessio Saltarin
'''

import fablepage
import os
import logging

from generators import chapter, templateloader

class EPubLoader(templateloader.TemplateLoader):
    
    def __init__(self, fable_id, lang, character):
        super(EPubLoader, self).__init__(fable_id, lang, character)
        
    def build(self):
        if self._buildFableFromFile():
            if len(self.paras) > 0:
                self.fable_doc = fablepage.EPubFableDoc(self._title, standalone=True)
                self.fable_doc.initialize(self._language.get_ISO())
                self._parseFile()
                self._addCover()
                self.fable_doc.addTitle(self._title)
                for chapter in self.chapters:
                    self._buildChapter(self.fable_doc, chapter)
            else:
                print 'CRITICAL Loader Error: empty contents.'
                raise
            self.fable_doc.build() 
            
    def _get_format(self):
        return '.epub'
    
    def get_images_path_to(self, filename):
        pics_folder = "F_PICS"
        if (self._character.sex == 'M'):
            pics_folder = "M_PICS"
        filepath_en = self._get_resources_path_lang()
        images_path = os.path.join(filepath_en, pics_folder)
        lang_code = self._language.language_code()
        if (lang_code != "EN"):
            finalpath_otherlang = os.path.normpath(os.path.join(filepath_en, lang_code))
            fullfilepath = os.path.join(finalpath_otherlang, pics_folder)
            path_to_file = os.path.join(fullfilepath, filename)
            if (os.path.isfile(path_to_file)):
                images_path = fullfilepath
        return os.path.join(images_path, filename)
            
    def __get_fable(self):
        return self.fable_doc
    
    def __get_epub_file(self):
        return self._ebook_file
    
    def _replace_tags(self):
        template_text = super(EPubLoader, self)._replace_tags()
        template_text = template_text.replace('<para alignment="center" fontsize="16">',
                                              '<span class="fableme1 fablemecenter">')
        template_text = template_text.replace('<para alignment="right" fontsize="16">',
                                              '<span class="fableme1 fablemeright">')
        template_text = template_text.replace('</para>', '</span>')
        return template_text 
            
    fable = property(__get_fable, doc="""Get the fable document.""")
    fable_file = property(__get_epub_file, doc="""Get fable ePUB file path.""")
        