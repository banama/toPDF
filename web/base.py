#coding:utf8
import tornado.web

class BaseHandle(tornado.web.RequestHandler):
	def ps(self):
		pass

class AuthHandle(tornado.web.RequestHandler):
    def require_login(self):
        if not self.get_cookie('username') and not self.get_cookie('account'):
            self.redirect('/login')