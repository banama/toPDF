import os
import sys
import base64
import uuid, os
from urllib import unquote
import img2pdf
import StringIO

class topdf(object):
    def __init__(self, base64img, width, height):
        self.base64img = base64img
        self.width = int(width)
        self.height = int(height)
        self.fileExt = str(uuid.uuid1())
    
    def topdf(self):
        self.f_pdf = self.fileExt+'.pdf'
        self.filename = self.fileExt + '.jpg'
        w = 612.0
        h = w * self.height / self.width
        self.codes = "".join(unquote(self.base64img).split(',')[1:])
        
        # static file (CDN)
        img = open(self.filename,'wb')
        img.write(base64.b64decode(self.codes))
        img.close()
        f = open(self.filename, 'r')
        print f.read() == base64.b64decode(self.codes)

        sd = img2pdf.convert([StringIO.StringIO(base64.b64decode(self.codes))], 150, x=620, y="")
        hand = open(self.f_pdf, 'wb')
        hand.write(sd)
        hand.close()
        #self.save_pdf()
        return self.f_pdf

    def save_pdf(self):
        with open(self.filename, 'r') as img_fp:
            sd = img2pdf.convert([img_fp], 150, x=620, y="")
            hand = open(self.f_pdf, 'wb')
            hand.write(sd)
            hand.close()