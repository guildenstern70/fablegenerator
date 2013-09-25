'''
PDFGenerator
fablepage.py

@author: Alessio Saltarin
'''

import loader
import stylesheet

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.units import cm


_W, _H = (21*cm, 29.7*cm) # This is the A4 size
_WF, _HF = (17*cm, 22*cm) # This is the size of a full size flowable
LEFT_MARGIN = 1.5*cm

pdfmetrics.registerFont(TTFont('Calibri', 'Calibri.ttf'))

def firstPages(canvas, doc):
    canvas.saveState()
    canvas.setFont("Calibri", 11)
    canvas.drawCentredString(_W/2, 820, 'FableMe - A fable for your child')
    canvas.setFont('Calibri', 9)
    canvas.drawCentredString(_W/2, 20, 'FableMe - http://www.fableme.com')
    canvas.restoreState()
    
def laterPages(canvas, doc):
    canvas.saveState()
    canvas.setFont('Calibri', 9)
    canvas.drawCentredString(_W/2, 50, '- %d -' % doc.page)
    canvas.restoreState()

class FableDoc():
    
    def __init__(self, docpath):
        self._doc = SimpleDocTemplate(docpath, pagesize=A4)
        self._story = [Spacer(1, 2*cm)]
        self._styles = stylesheet.fableMeStyleSheet()
        
    def addCover(self, coverImageFile):
        image = Image(coverImageFile, _WF, _HF)
        image.vAlign = 'TOP'
        self._story.append(image)
        self._story.append(PageBreak())
        
    def getImageFromText(self, imageTextDescription):
        image = None
        try:
            if (imageTextDescription[5] == '['):
                imageFileDesc = imageTextDescription[6:imageTextDescription.find(']')].split(',')
                imageFileName = loader.resource_path(imageFileDesc[0])
                imageFileWidth = float(imageFileDesc[1])
                imageFileHeight = float(imageFileDesc[2])
                image = Image(imageFileName, imageFileWidth*cm, imageFileHeight*cm)
        except:
            print 'Cannot parse image descriptor: ' + imageTextDescription
        return image
        
    def addTitle(self, text):
        p = Paragraph(text, self._styles["Title"])
        self._story.append(p)
        self._story.append(Spacer(1, 2.2*cm))
        
    def addChapterTitle(self, chapter_title):
        p = Paragraph(chapter_title, self._styles['Chapter'])
        self._story.append(p)
        
    def addPageBreak(self):
        self._story.append(PageBreak())
        
    def addParagraphOrImage(self, text):
        if (text.startswith('**IMG')):
            flowable = self.getImageFromText(text)
        else:
            flowable = Paragraph(text, self._styles["Normal"])
        if (flowable != None):
            self._story.append(flowable)
            self._story.append(Spacer(1, 0.2*cm))
        else:
            print '*Warning: image is None!'
        
    def save(self):
        self._doc.build(self._story, onFirstPage=firstPages, onLaterPages=laterPages)
        
        
        
    
    