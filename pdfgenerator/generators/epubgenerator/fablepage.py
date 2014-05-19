'''
PDFGenerator
epubgenerator.fablepage.py

@author: Alessio Saltarin
'''

import codecs
import os
import zipfile
import sys
import logging
import shutil

import generators.textformatter as textformatter

EPUB_SOURCES_DIR = "resources/epubfiles"
EPUB_OUTPUT_DIR = "../output"
EPUB_MASTER_FILE = "index.html"
EPUB_PROTO_FILE = "index_prototype.html"
PAGE_BREAK = "<div style='page-break-before:always;'></div>"

# TO DO: Content.odf
# TO DO: Fix cover

class EPubFableDoc(textformatter.TextFormatter):
    
    def __init__(self, fabletitle, standalone):
        self._story = ""
        self._language = "en-US";
        self._title = fabletitle
                
    def setInitialXHTML(self, iso_language):
        logging.debug('-- EPUB loading initial XHTML ')
        in_file_full_path = os.path.join(EPUB_SOURCES_DIR, EPUB_PROTO_FILE)
        in_file = open(in_file_full_path,"r")
        xhtmlContents = in_file.read()
        in_file.close()
        self._story = xhtmlContents.replace('{iso_lang}', iso_language)
        self._story = self._story.replace('{title}', self._title)
    
    def addCover(self, coverImageFile):
        logging.debug('-- EPUB addCover')
        cover_template = """<p class="fableme1"><img src="{coverfile}" alt="Cover" class="fableme2"/></p>"""
        cover_template = cover_template.replace('{coverfile}', coverImageFile)
        cover_template += PAGE_BREAK
        self._story += cover_template
    
    def prepareImageFromText(self, imageTextDescription, loader):
        logging.debug('-- EPUB getImageFromText')
        imageFileName = None
        try:
            if (imageTextDescription[5] == '['):
                imageFileName = imageTextDescription[6:imageTextDescription.find(']')].split(',')
                imageFilePath = loader.get_images_path_to(imageFileName[0])
                logging.debug('Copying '+imageFilePath+' to > '+ EPUB_SOURCES_DIR + '...')
                logging.debug('Done.')
                shutil.copy(imageFilePath, EPUB_SOURCES_DIR)
                #imageFileWidth = float(imageFileDesc[1])
                #imageFileHeight = float(imageFileDesc[2])
        except:
            logging.critical('Cannot parse image descriptor: ' + imageTextDescription)
        return imageFileName[0]
    
    def addTitle(self, text):
        logging.debug('-- EPUB addTitle')
        _template = """<p class="fableme1">{title}</p>"""
        _template = _template.replace('{title}', text)
        _template += PAGE_BREAK
        self._story += _template
    
    def addChapterTitle(self, chapter_title):
        logging.debug('-- EPUB addChapterTitle')
        _template = """<p class="fableme1"<i class="fableme4">{chaptertitle}</i></p>"""
        _template = _template.replace('{chaptertitle}', chapter_title)
        _template += """<p class="fableme1">&nbsp;</p>"""
        self._story += _template
    
    def addPageBreak(self):
        logging.debug('-- EPUB addPageBreak')
        self._story += PAGE_BREAK
    
    def addParagraphOrImage(self, text, loader):
        logging.debug('-- EPUB addParagraphOrImage')
        if (text.startswith('**IMG')):
            imageName = self.prepareImageFromText(text, loader)    
            _template = """<p class="fableme1"><img src="{image_src}" alt="Image" class="fableme2"/></p>"""
            _template = _template.replace('{image_src}', imageName)
        else:
            _template = """<p class="fableme1">{ptext}</p>"""
            _template = _template.replace('{ptext}', text)
        if (_template != None):
            self._story += _template
        else:
            logging.critical('*Warning: image is None!')
            
    def closeXHTML(self):
        self._story += """<p class="fableme1"><i class="fableme4">The End</i></p>
                          <p class="fableme1">&nbsp;</p></body></html>"""
    
    def build(self):
        logging.debug('-- EPUB BUILD')
        self.closeXHTML()
        old_path = os.getcwd()
        os.chdir(EPUB_SOURCES_DIR)
        try:
            if os.path.isfile(EPUB_MASTER_FILE):
                logging.debug('-- Deleting old index.html...')
                os.remove(EPUB_MASTER_FILE)
            logging.debug('-- Saving new index.html...')
            xhtml_file = codecs.open(EPUB_MASTER_FILE, "w", "utf-8")
            xhtml_file.write(self._story)
            xhtml_file.close()
            logging.debug('-- Done.')
        except:
            logging.error('Error saving ePub Zip file')
            logging.error('Unexpected error: ' + str(sys.exc_info()[0]))
        os.chdir(old_path)

    def save(self, epub_fullname):
        epub_absolute = os.path.join(os.getcwd(), epub_fullname)
        logging.debug(' - EPUB SAVE Writing ePub file: %s', epub_absolute)
        os.chdir(EPUB_SOURCES_DIR)
        if self.zip_files(epub_absolute):
            logging.debug(' - ePub file created successfully.')
        os.chdir('..')
        logging.debug(' - Done.')
    
    def zip_files(self, zip_file):
        save_succeeded = True
        try:
            if os.path.isfile(EPUB_MASTER_FILE):
                if os.path.isfile(zip_file):
                    logging.debug(' - Removing existing old '+zip_file)
                    os.remove(zip_file)
                with zipfile.ZipFile(zip_file, 'w') as fzip:
                    # First, add mimetype
                    for root, _, files in os.walk("."):
                        for cfile in files:
                            fpath = os.path.join(root, cfile)
                            if (fpath == ".\mimetype"):
                                fzip.write(fpath)
                                logging.debug(' - Adding '+fpath)
                    
                    # Second, add all other files
                    for root, _, files in os.walk("."):
                        for cfile in files:
                            fpath = os.path.join(root, cfile)
                            if (fpath != ".\mimetype"):
                                logging.debug(' - Adding '+fpath)
                                fzip.write(fpath, compress_type=zipfile.ZIP_DEFLATED)
            else:
                logging.debug('Cannot find epub XHTML. Wrong dir?')
                save_succeeded = False
        except:
            logging.error('Error saving ePub Zip file')
            logging.error('Unexpected error: ' + sys.exc_info()[0])
            save_succeeded = False
        return save_succeeded
            
    
    