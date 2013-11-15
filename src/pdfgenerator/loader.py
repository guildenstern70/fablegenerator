'''
PDFGenerator
loader.py

@author: Alessio Saltarin
'''

import sys
import os
import fablepage
import fables
import chapter
import tagreplacer
import languages

OUTPUT_DIR = "../output/"
RESOURCES_DIR = "../resources/"
        
def output_path(name):
    return os.path.join(OUTPUT_DIR, name)

def resource_path(name):
    return os.path.join(RESOURCES_DIR, name)

class FableLoader(object):
    
    def __init__(self, fable_id, lang, sex, name):
        self._fable_id = fable_id
        self._set_variables(lang, sex, name)
        
    def build(self):
        if self._readFile():
            if len(self.paras) > 0:
                self.fable_doc = fablepage.FableDoc(self._title)
                self._parseFile()
                self._addCover()
                self.fable_doc.addTitle(self._title)
                for chapter in self.chapters:
                    self._buildChapter(self.fable_doc, chapter)
            else:
                print 'CRITICAL PDF Error: empty contents.'
                raise
            self.fable_doc.build() 
        
    def save(self):
        saved = True
        try:
            if (self.fable_doc):
                self.fable_doc.save(self._pdffile)
            else:
                print '*** ABORTING'
                saved = False
        except:
            saved = False
        return saved
        
    def get_resources_path_to(self, filename):
        return os.path.join(self._get_resources_path(), filename) 
        
    def get_images_path_to(self, filename):
        pics_folder = "F_PICS"
        if (self._sex == 'M'):
            pics_folder = "M_PICS"
        images_path = os.path.join(self._get_resources_path(), pics_folder)
        return os.path.join(images_path, filename)
    
    def _get_resources_path(self):
        """ Get the relative path to filename, ie: ../resources/My_voyage_to_Aragon/My_voyage_to_Aragon.txt """
        fable_dir = self._template['template_dir']
        lang_code = self._language.language_code()
        filepath = resource_path(fable_dir)
        if (lang_code != "EN"):
            filepath = os.path.join(filepath, lang_code)
        return os.path.normpath(filepath)
        
    def _set_variables(self, lang, sex, name):
        self._language = self._set_language(self._fable_id, lang)
        self._template = fables.get_book_template(self._fable_id)
        self._filename = self._template['template_text_file']
        self._pdffile = output_path(self._filename[:-4] + '.pdf')
        self._title = self._template[self._language.get_title_key()]
        print '-- Creating fable = ' + self._title
        self._sex = sex
        self._name = name
        self.fable_doc = None
        self.chapters = []
               
    def _set_language(self, filename, lang):
        lang = languages.Language(lang)
        print '-- Setting language = ' + lang.language()
        return lang

    def _replace_tags(self, filecontents):
        """ Get the final fable as a long string """
        print '-- Replacing tags...'
        replacer = tagreplacer.Replacer(filecontents, self._sex, self._name)
        replacements = replacer.get_replacements()
        for tag, val in replacements.items():
            if ((val != None) and (len(val)>0)):
                filecontents = filecontents.replace(tag, val)
        return filecontents
    
    def _readFile(self):
        """ Transfer file contents into paragraphs list """
        fileReadOk = True
        fileFullPath = self.get_resources_path_to(self._filename)
        print '-- Reading file ' + fileFullPath
        try:
            fileobj = open(fileFullPath, "r")
            filecontents = self._replace_tags(fileobj.read())
            fileobj.close()
            self.paras = filecontents.split('\n')
            print '-- The file has ' + str(len(self.paras)) + ' paragraphs.'
        except IOError:
            print '*** Critical error opening %s' % fileFullPath
            print '*** ', sys.exc_info()
            fileReadOk = False
        return fileReadOk
                
    def _parseFile(self):
        """ Divide paragraphs in chapters """
        chapter_paragraphs = []
        chapter_nr = 1
        for paragraph in self.paras:
            if (self._language.is_beginning_of_chapter(paragraph)):
                if (len(chapter_paragraphs) > 0):
                    self._addChapter(chapter_paragraphs)
                    chapter_nr += 1
                    chapter_paragraphs = []
            chapter_paragraphs.append(paragraph)       
        
    def _addCover(self):
        unix_name = self._filename[:-4] + '.jpg'
        cover_filepath = self.get_images_path_to(unix_name)
        self.fable_doc.addCover(cover_filepath)
                
    def _addChapter(self, paragraphs):
        """ Add a chapter to chapters list """
        new_chapter = chapter.FableChapter()
        new_chapter.title = paragraphs[0]
        for i in range(1,len(paragraphs)):
            new_chapter.addParagraph(paragraphs[i])
        self.chapters.append(new_chapter)
            
    def _buildChapter(self, fable, chapter):
        fable.addChapterTitle(chapter.title)
        for paragraph in chapter.paragraphs:
            fable.addParagraphOrImage(paragraph, self)
        fable.addPageBreak()
                
    def __get_fable(self):
        return self.fable_doc
    
    def __get_pdf_file(self):
        return self._pdffile
        
    fable = property(__get_fable, doc="""Get the fable document.""")
    fable_file = property(__get_pdf_file, doc="""Get fable PDF file path.""")
        

        