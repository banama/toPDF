#coding:utf8
import tornado.ioloop
import tornado.web

class index(tornado.web.RequestHandler):
	def get(self):
		self.write('hello')
	def post(self):
		img = self.get_argument('img')
		print img
		self.write(img)

application = tornado.web.Application([
	(r"/", index)
])

if __name__ == '__main__':
	application.listen(8888)
	tornado.ioloop.IOLoop.instance().start()