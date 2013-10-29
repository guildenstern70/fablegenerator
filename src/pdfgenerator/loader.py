'''
PDFGenerator
loader.py

@author: Alessio Saltarin
'''

import sys
import os
import fablepage
import chapter
import tagreplacer

OUTPUT_DIR = "../output/"
RESOURCES_DIR = "../resources/"
        
def output_path(name):
    return os.path.join(OUTPUT_DIR, name)

def resource_path(name):
    return os.path.join(RESOURCES_DIR, name)

class FableLoader(object):
    
    def __init__(self, filename, sex, name):
        self._filename = filename
        self._pdffile = output_path(self._filename[:-4] + '.pdf')
        self._title = self._get_title()
        self._sex = sex
        self._name = name
        self.fable_doc = None
        self.chapters = []
              
    def _get_title(self):
        title = self._filename.replace('_', ' ')
        return title[:-4]

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
        print '  Reading file ' + self._filename
        try:
            fileobj = open(resource_path(self._filename), "r")
            filecontents = self._replace_tags(fileobj.read())
            fileobj.close()
            self.paras = filecontents.split('\n')
            print '  The file has ' + str(len(self.paras)) + ' paragraphs.'
        except IOError:
            print '*** Critical error opening ', self._filename
            print '*** ', sys.exc_info()[0]
            fileReadOk = False
        return fileReadOk
                
    def build(self):
        self._readFile()
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
        self.fable_doc.save(self._pdffile)
        
    def _parseFile(self):
        """ Divide paragraphs in chapters """
        chapter_paragraphs = []
        chapter_nr = 1
        for paragraph in self.paras:
            if ((paragraph.startswith('Chapter') or (paragraph.startswith('END-OF-FILE')))):
                if (len(chapter_paragraphs) > 0):
                    self._addChapter(chapter_paragraphs)
                    chapter_nr += 1
                    chapter_paragraphs = []
            chapter_paragraphs.append(paragraph)       
        
    def _addCover(self):
        template = self._get_title()
        unix_name = template.replace(' ', '_')
        cover_filepath = resource_path(unix_name + '.jpg')
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
            fable.addParagraphOrImage(paragraph)
        fable.addPageBreak()
                
    def __get_fable(self):
        return self.fable_doc
    
    def __get_pdf_file(self):
        return self._pdffile
        
    fable = property(__get_fable, doc="""Get the fable document.""")
    fable_file = property(__get_pdf_file, doc="""Get fable PDF file path.""")
        

        