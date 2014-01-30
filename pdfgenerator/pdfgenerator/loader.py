'''
PDFGenerator
loader.py

@author: Alessio Saltarin
'''

import sys
import codecs
import os.path
import fablepage
import fables
import chapter
import tagreplacer
import languages
import utils
import logging
        
class SimpleLoader(object):
    
    def __init__(self, fable_id, lang, character):
        self._fable_id = fable_id
        self._set_variables(lang, character)
        
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
    
    def _get_resources_path(self):
        fable_dir = self._template['template_dir']
        lang_code = self._language.language_code()
        filepath = utils.BasicUtils.get_from_relative_resources(fable_dir)
        if (lang_code != "EN"):
            filepath = os.path.join(filepath, lang_code)
        return utils.BasicUtils.get_from_resources(filepath)

    def _get_resources_path_lang(self):
        fable_dir = self._template['template_dir']
        filepath_en = utils.BasicUtils.get_from_relative_resources(fable_dir)
        finalpath = os.path.normpath(filepath_en)
        return finalpath
        
    def _set_variables(self, lang, character):
        self._language = self._set_language(self._fable_id, lang)
        self._template = fables.get_book_template(self._fable_id)
        self._filename = self._template['template_text_file']
        self._pdffile = utils.BasicUtils.get_output_path(self._filename[:-4] + '_' + self._language.language_code() + '.pdf')
        self._title = self._template[self._language.get_title_key()]
        try:
            print '-- Creating fable = ' + self._title
        except:
            print '-- Creating fable document'
        self._character = character
        self.fable_doc = None
        self.chapters = []
               
    def _set_language(self, filename, lang):
        return languages.Language(lang)

    def _replace_tags(self, filecontents):
        print '-- Replacing tags...'
        replacer = tagreplacer.Replacer(filecontents, self._character)
        replacements = replacer.get_replacements()
        for tag, val in replacements.items():
            if ((val != None) and (len(val)>0)):
                filecontents = filecontents.replace(tag, val)
        return filecontents
    
    def _readFile(self):
        fileReadOk = True
        fileFullPath = self.get_resources_path_to(self._filename)
        print '-- Reading file ' + fileFullPath
        try:
            fileobj = codecs.open(fileFullPath, "r", "utf-8")
            ufilecontents = unicode(fileobj.read())
            filecontents = self._replace_tags(ufilecontents)
            fileobj.close()
            self.paras = filecontents.split('\n')
            print '-- The file has ' + str(len(self.paras)) + ' paragraphs.'
        except IOError:
            print '*** Critical error opening %s' % fileFullPath
            print '*** ', sys.exc_info()
            fileReadOk = False
        return fileReadOk
                
    def _parseFile(self):
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
    
    
class GoogleLoader(SimpleLoader):
    
    def save(self, file_h):
        saved = True
        try:
            if (self.fable_doc):
                self.fable_doc.save(file_h)
            else:
                logging.debug('Aborting PDF save: fable_doc is null.')
                saved = False
        except:
            saved = False
        return saved
    
    def get_resources_path_to(self, filename):
        return utils.GoogleUtils.get_from_resources(filename)
    
    def get_images_path_to(self, filename):
        pics_folder = "F_PICS"
        if (self._character.sex == 'M'):
            pics_folder = "M_PICS"
        image_file = os.path.join(pics_folder, filename)
        return utils.GoogleUtils.get_from_resources(image_file)
    
    def _get_resources_path(self):
        fable_dir = self._template['template_dir']
        lang_code = self._language.language_code()
        filepath = utils.GoogleUtils.get_from_relative_resources(fable_dir)
        if (lang_code != "EN"):
            filepath = utils.GoogleUtils.get_from_relative_resources(filepath, lang_code)
        return utils.GoogleUtils.get_from_resources(filepath)
    
    def setContents(self, filecontents):
        filecontents = self._replace_tags(filecontents)
        self.paras = filecontents.split('\n')
        

    
    
    
    
        

        