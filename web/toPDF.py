import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import base64
import uuid

 
def topdf(code):
	fileExt = str(uuid.uuid1())
 	f_pdf = fileExt+'.pdf'
 	filename = code + '.png'
 	w, h = letter	
 	c = canvas.Canvas(f_pdf, pagesize = letter)
 
 	print code
 	codes = code.split(',')[1] 
 	img = open('filename','wb')
	img.write(base64.b64decode(codes))
	img.close()
 	c.drawImage(filename, 0, 0, w, h)
 	c.save()
	return f_pdf
 
