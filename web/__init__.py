#coding:utf8
import tornado.web
import tornado.ioloop
from toPDF import topdf
import os

# import tornado.wsgi
# import sae
# import tornado

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
        self.write(_topdf.topdf())

class exsit(tornado.web.RequestHandler):
    def post(self):
        pdfcode = self.get_argument('pdfcode')
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