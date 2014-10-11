#coding:utf8
import tornado.web
from base import AuthHandle
import db

class me(AuthHandle):
    def get(self):
        self.require_login()
        user = (lambda: self.get_cookie('username') and  self.get_cookie('username') or self.get_cookie('account'))()
        pdflist = db.mdb('topdf', 'pdf').perform()
        if self.get_cookie('username'):
        	lists = list(pdflist.find({'username': user}).limit(10))
        else:
        	lists = list(pdflist.find({'account': user}).limit(10))
        self.render('people.html', user = ''.join(user), lists = lists)

class save(AuthHandle):
    def post(self):
        self.require_login()
        pdfmark = ''.join(self.get_arguments('pdfmark'))
        user = (lambda: self.get_cookie('username') and  self.get_cookie('username') or self.get_cookie('account'))()
        pdflist = db.mdb('topdf', 'pdf').perform()
        if self.get_cookie('username'):
        	pdflist.insert({'username': user, 'pdf': pdfmark})
        else:
        	pdflist.insert({'account': user, 'pdf': pdfmark})
        self.write('t')


