#coding:utf8
import tornado.web
import tornado.ioloop
from toPDF import topdf
import os
import auth
import people
import base
import db

class version(tornado.web.RequestHandler):
    def get(self):
        self.write(tornado.version)

class index(tornado.web.RequestHandler):
    def get(self):
        if self.get_cookie('username') or self.get_cookie('account'):
            login = '我的文档'
        else:
            login = '登录'
        self.render('index.html', login = login)

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
        pdfexsit = db.mdb('topdf', 'pdfexsit').perform()
        if pdfexsit.find_one({'pdf': pdfcode}) == None:
            self.write('f')
        else:
            self.write('t')

settings = dict(
    template_path=(os.path.join(os.path.dirname(__file__), "templates")),
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    debug=True,
    cookie_secret = "dskfhisdjklagkfdklag;lkjasdklgjkldsjaklgjkldsfksdklf"
)

application = tornado.web.Application(
    handlers = [
        (r"/", index),
        (r"/pdf/([0-9a-zA-Z\-]*)", pdf),
        (r"/exsit", exsit),
        (r"/join", auth.join),
        (r"/login", auth.login),
        (r"/logout", auth.logout),
        (r"/oauth/(\w+)", auth.oauth),
        (r"/jump/(\w+)", auth.jump),
        (r"/people", people.me),
        (r'/pdflist', people.pdflist),
        (r"/save", people.save),
        (r"/remark", people.remark),
        (r"/delete", people.delete),
        (r"/test", auth.test),
        ],**settings
    )

if __name__ == '__main__':
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()