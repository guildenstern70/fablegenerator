""" 
 
 PdfGenerator
 
 loaderfactory.py
 
"""

import pdfgenerator.loader as pdf_loader
import epubgenerator.loader as epub_loader

def LoaderFactory(e_format, fable_id, tlang, character, use_google = False):
    loader = None
    if (e_format == 'PDF'):
        if (use_google):
            loader = pdf_loader.GoogleLoader(fable_id, tlang, character)
        else:
            loader = pdf_loader.SimpleLoader(fable_id, tlang, character)
    else:
        loader = epub_loader.EPubLoader(fable_id, tlang, character)
    return loader


        
    