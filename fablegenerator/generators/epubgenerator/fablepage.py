'''
FableGenerator
epubgenerator.fablepage.py

@author: Alessio Saltarin
'''

import codecs
import glob
import os
import sys
import logging
import shutil
import zipfile

import generators.textformatter as textformatter
import epubheaders

EPUB_SOURCES_DIR = "resources/epubfiles"
EPUB_OUTPUT_DIR = "../output"
EPUB_MASTER_FILE = "index.html"
EPUB_PROTO_FILE = "index_prototype.html"
EPUB_INDEX_FILE = "content.opf"
PAGE_BREAK = "<div style='page-break-before:always;'></div>"

# TO DO: Content.opf
# TO DO: Fix cover

class EPubFableDoc(textformatter.TextFormatter):
    
    def __init__(self, fabletitle, standalone):
        self._story = ""
        self._index = ""
        self._id_counter = 1
        self._language = "en-US";
        self._title = fabletitle
        
    def initialize(self, iso_language):
        self._cleanAll()
        self._setInitialXHTML(iso_language)
        self._setInitialIndex(iso_language)
        
    def addCover(self, coverImageFile):
        new_path = os.path.join(EPUB_SOURCES_DIR, 'cover.jpeg')
        try:
            if os.path.isfile('cover.jpeg'):
                logging.debug('-- Deleting old cover.jpeg...')
                os.remove('cover.jpeg')
            shutil.copy(coverImageFile, new_path)
            self._index += """   <item href="cover.jpeg" id="cover" media-type="image/jpeg"/>"""
        except:
            logging.error('Error copying cover file')
            logging.error('Unexpected error: ' + str(sys.exc_info()[1]))
    
    def prepareImageFromText(self, imageTextDescription, loader):
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
    
    def addTitle(self, text, dedication):
        _template = """<p class="fableme1">&#160;</p><p class="fableme4 fablemecenter">FableMe.com</p>
        <div class="booktitle">{title}</div><p class="fableme1">&#160;</p>
        <p class="fableme1">&#160;</p><p class="fableme1">&#160;</p>
        <p class="fableme4 fablemecenter">{dedication}</p>"""
        _template = _template.replace('{title}', text)
        dedicPar = ""
        for dedicLine in dedication.split('***'):
            dedicPar += dedicLine
            dedicPar += "<br/>"
        _template = _template.replace('{dedication}', dedicPar)
        _template += PAGE_BREAK
        self._index = self._index.replace('{title}', text)
        self._story += _template
    
    def addChapterTitle(self, chapter_title):
        _template = """<div class="chaptertitle"><p class="fableme1">&#160;</p><i class="fableme4">{chaptertitle}</i></div>"""
        _template = _template.replace('{chaptertitle}', chapter_title)
        _template += """<p class="fableme1">&#160;</p>"""
        self._story += _template
    
    def addPageBreak(self):
        self._story += PAGE_BREAK
    
    def addParagraphOrImage(self, text, loader):
        if (text.startswith('**IMG')):
            self._id_counter += 1
            idname = 'id' + str(self._id_counter)
            imageName = self.prepareImageFromText(text, loader)    
            _template = """<div class="fableimage">
            <img alt="Image" src="{image_src}"/>
            </div>"""
            _template = _template.replace('{image_src}', imageName)
            _index = """<item href="{imagefilename}" id="{imgid}" media-type="image/jpeg"/>"""
            _index = _index.replace('{imagefilename}', imageName)
            _index = _index.replace('{imgid}', idname)
            self._index += _index
        else:
            _template = """<p class="fableme1">{ptext}</p>"""
            _template = _template.replace('{ptext}', text)
        if (_template != None):
            self._story += _template
        else:
            logging.critical('*Warning: image is None!')
            
    def closeXHTML(self):
        self._story += """</body></html>"""
        self._index += epubheaders.EPUB_INDEX_FOOTER
        
    def build(self):
        logging.debug('-- EPUB BUILD')
        self.closeXHTML()
        old_path = os.getcwd()
        os.chdir(EPUB_SOURCES_DIR)
        self._createNewFile(EPUB_MASTER_FILE, self._story)
        self._createNewFile(EPUB_INDEX_FILE, self._index)
        os.chdir(old_path)

    def save(self, epub_fullname):
        epub_absolute = os.path.join(os.getcwd(), epub_fullname)
        logging.debug(' - EPUB SAVE Writing ePub file: %s', epub_absolute)
        old_path = os.getcwd()
        os.chdir(EPUB_SOURCES_DIR)
        if self.zip_files(epub_absolute):
            logging.debug(' - ePub file created successfully.')
        os.chdir(old_path)
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
                                logging.debug('ZIP - Adding '+fpath)
                    
                    # Second, add all other files
                    for root, _, files in os.walk("."):
                        for cfile in files:
                            fpath = os.path.join(root, cfile)
                            if (fpath != ".\mimetype"):
                                logging.debug('ZIP - Adding '+fpath)
                                fzip.write(fpath, compress_type=zipfile.ZIP_DEFLATED)
            else:
                logging.debug('Cannot find epub XHTML. Wrong dir?')
                save_succeeded = False
        except:
            logging.error('Error saving ePub Zip file')
            logging.error('Unexpected error: ' + str(sys.exc_info()[1]))
            save_succeeded = False
        return save_succeeded
    
    def _setInitialXHTML(self, iso_language):
        xhtmlContents = epubheaders.EPUB_XHTML_HEADER
        self._story = xhtmlContents.replace('{iso_lang}', iso_language)
        self._story = self._story.replace('{title}', self._title)
        
    def _setInitialIndex(self, language):
        self._index = epubheaders.EPUB_INDEX_HEADER
        self._index = self._index.replace('{language}', language)
        
    def _cleanAll(self):
        logging.debug('-- Cleaning ')
        old_path = os.getcwd()
        os.chdir(EPUB_SOURCES_DIR)
        for fl in glob.glob("./*.jpg"):
            logging.debug('-- Removing ' + str(fl))
            os.remove(fl)
        os.chdir(old_path)
        
    def _createNewFile(self, filename, filecontents):
        try:
            if os.path.isfile(filename):
                logging.debug('-- Deleting old index.html...')
                os.remove(filename)
            logging.debug('-- Saving new '+ filename + '...')
            xhtml_file = codecs.open(filename, "w", "utf-8")
            xhtml_file.write(filecontents)
            xhtml_file.close()
            logging.debug('-- Done.')
        except:
            logging.error('Error saving file '+ filename)
            logging.error('Unexpected error: ' + str(sys.exc_info()[0]))
            
    
    