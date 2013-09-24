'''
PDFGenerator
FablePage.py

@author: Alessio Saltarin
'''

import stylesheet

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import cm


_W, _H = (21*cm, 29.7*cm) # This is the A4 size
LEFT_MARGIN = 1.5*cm

pdfmetrics.registerFont(TTFont('Calibri', 'Calibri.ttf'))

def firstPages(canvas, doc):
    canvas.saveState()
    canvas.setFont("Calibri", 11)
    canvas.drawCentredString(_W/2, 800, 'FableMe - A fable for your child')
    canvas.setFont('Calibri', 9)
    canvas.drawCentredString(_W/2, 800, 'http://www.fableme.com')
    canvas.restoreState()
    
def laterPages(canvas, doc):
    canvas.saveState()
    canvas.setFont('Calibri', 9)
    canvas.drawString(cm, LEFT_MARGIN, "Page %d %s" % (doc.page, 'FableMe.com'))
    canvas.restoreState()

class FableDoc():
    
    def __init__(self, docpath):
        self._pageinfo = 'FableMe.com'
        self._doc = SimpleDocTemplate(docpath, pagesize=A4)
        self._story = [Spacer(1, 2*cm)]
        self._styles = stylesheet.fableMeStyleSheet()
        
    def addTitle(self, text):
        p = Paragraph(text, self._styles["Title"])
        self._story.append(p)
        self._story.append(Spacer(1, 2.2*cm))
        
    def addChapter(self, chapter_number, chapter_title):
        title = chapter_number + '. ' + chapter_title 
        p = Paragraph(title, self._styles['Chapter'])
        self._story.append(p)
        self._story.append(Spacer(1, 0.2*cm))
        
    def addParagraph(self, text):
        p = Paragraph(text, self._styles["Normal"])
        self._story.append(p)
        self._story.append(Spacer(1, 0.2*cm))
        
    def addImage(self, image_path, x, y, width, height):
        self._c.drawImage(image_path, x, y, width, height, mask=None)
        
    def save(self):
        self._doc.build(self._story, onFirstPage=firstPages, onLaterPages=laterPages)
        
        
        
    
    