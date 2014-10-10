#coding:utf8
import tornado.web
from auth import authmiddler

class me(authmiddler):
    def get(self):
        self.require_login()
        self.render('people.html')