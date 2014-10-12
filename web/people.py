#coding:utf8
import tornado.web
from base import AuthHandle
import db
import json

class me(AuthHandle):
    def get(self):
        self.require_login()
        user = (lambda: self.get_cookie('username') and  self.get_cookie('username') or self.get_cookie('account'))()
        self.render('people.html', user = ''.join(user))

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

class pdflist(AuthHandle):
    def get(self):
        self.require_login()
        user = (lambda: self.get_cookie('username') and  self.get_cookie('username') or self.get_cookie('account'))()
        pdflist = db.mdb('topdf', 'pdf').perform()
        if self.get_cookie('username'):
            _lists = pdflist.find({'username': user})
            lists = []
            for i in _lists:
                if 'remark' in i:
                    lists.append([i['remark'], i['pdf']])
                else:
                    lists.append(['', i['pdf']])
            self.write(json.dumps({'pdflist': lists}))
        else:
            _lists = pdflist.find({'account': user})
            lists = []
            for i in _lists:
                if 'remark' in i:
                    lists.append([i['remark'], i['pdf']])
                else:
                    lists.append(['', i['pdf']])
            self.write(json.dumps({'pdflist': lists}))

class remark(AuthHandle):
    def post(self):
        self.require_login()
        pdfmark = ''.join(self.get_arguments('pdfmark')).encode('utf8')
        remarks = ''.join(self.get_arguments('remarks')).encode('utf8')

        pdf = db.mdb('topdf', 'pdf').perform()
        user = (lambda: self.get_cookie('username') and  self.get_cookie('username') or self.get_cookie('account'))()
        _pdf = pdf.find_one({'pdf': pdfmark})

        if _pdf['pdf'] == None:
            self.write('f')
            return

        if self.get_cookie('username'):
            if _pdf['username'] != user:
                self.write('f')
            else:
                pdf.update({'pdf': pdfmark}, {'$set': {'remark': remarks}})
            # set cache
        else:
            if _pdf['account'] != user:
                self.write('f')
            else:
                pdf.update({'pdf': pdfmark}, {'$set': {'remark': remarks}})
            # set cache
        self.write('t')

class delete(AuthHandle):
    def post(self):
        self.require_login()
        pdfmark = ''.join(self.get_arguments('pdfmark')).encode('utf8')
        user = (lambda: self.get_cookie('username') and  self.get_cookie('username') or self.get_cookie('account'))()
        pdf = db.mdb('topdf', 'pdf').perform()
        pdfexsit = db.mdb('topdf', 'pdfexsit').perform()
        _pdf = pdf.find_one({'pdf': pdfmark})

        if _pdf['pdf'] == None:
            self.write('f')
            return

        if self.get_cookie('username') and _pdf['username'] == user:
            pdf.remove({'pdf': _pdf['pdf']})
            pdfexsit.remove({'pdf': _pdf['pdf']})
        else:
            pdf.remove({'pdf': _pdf['pdf']})
            pdfexsit.remove({'pdf': _pdf['pdf']})
        self.write('t')





