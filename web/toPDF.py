import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import base64
import uuid, os
from urllib import unquote

class topdf(object):
	def __init__(self, base64img, width, height):
		self.base64img = base64img
		self.width = int(width)
		self.height = int(height)
	
	def topdf(self):
		fileExt = str(uuid.uuid1())
	 	f_pdf = fileExt+'.pdf'
	 	filename = fileExt + '.png'
	 	w = 612.0
	 	h = w * self.height / self.width
	 	c = recanvas(f_pdf, pagesize = (w, h))
	 
	 	codes = "".join(unquote(self.base64img).split(',')[1:])
	 	
	 	# static file (CDN)
	 	img = open(filename,'wb')
		img.write(base64.b64decode(codes))
		img.close()
	 	c.drawImage(filename, 0, 0, w, h)
	 	c.save()

		return fileExt

def utf8str(x):
    if isinstance(x,unicode):
        return x.encode('utf8')
    else:
        return str(x)

def SaveToFile(filename, canvas, pdfdata):
        if hasattr(getattr(filename, "write",None),'__call__'):
            myfile = 0
            f = filename
            filename = utf8str(getattr(filename,'name',''))
        else :
            myfile = 1
            filename = utf8str(filename)
            f = open(filename, "wb")
        f.write(pdfdata)
        if myfile:
            f.close()
        if getattr(canvas,'_verbosity',None): print 'saved', filename

class recanvas(canvas.Canvas):
    def save(self):
        if len(self._code): self.showPage()
        pdfdata = self.getpdfdata()
        SaveToFile(self._filename, self, pdfdata)
 

