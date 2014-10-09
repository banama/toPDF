#coding:utf8
import tornado.web
import tornado.ioloop
from toPDF import topdf
import os


class version(tornado.web.RequestHandler):
    def get(self):
        self.write(tornado.version)

class index(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html', pdf = "_topdf.topdf()")

    def post(self):
        img = self.get_argument('img')
        width = self.get_argument('width')
        height = self.get_argument('height')
        _topdf = topdf(img, width=width, height=height)
        self.write(_topdf.topdf().split('.')[0])

class pdf(tornado.web.RequestHandler):
    def get(self, input):
        if input == "1":
            mark = False
            self.render('pdf.html', mark = mark)
        else:
            mark = True
            pdfurl = 'http://topdfs-pdf.stor.sinaapp.com/pdf/' + input + '.pdf'
            self.render('pdf.html', pdf = pdfurl, mark = mark)

class exsit(tornado.web.RequestHandler):
    def post(self):
        pdfcode = self.get_argument('pdfcode')
        if pdfcode == '1':
            self.write('f')
        else:
            self.write('t')

class Show(tornado.web.RequestHandler):
    def post(self):
        code = self.get_argument('pdf')
        print os.path.join('static/pdf', code + '.pdf')
        pdfs = os.path.join('static/pdf', code + '.pdf')
        self.render('showpdf.html', 
            pdf=code,
            pdf_url=pdfs
            )

application = tornado.web.Application(
    handlers = [
        (r"/", index),
        (r"/pdf/([0-9a-zA-Z\-]*)", pdf),
        (r"/exsit", exsit),
        (r"/show", Show)
        ],
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    debug=True
    )

if __name__ == '__main__':
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()