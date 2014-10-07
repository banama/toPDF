#coding:utf8
import tornado.ioloop
import tornado.web
from toPDF import topdf

class index(tornado.web.RequestHandler):
	def get(self):
		self.write('hello')
	def post(self):
		img = self.get_argument('img')
		print img
		filename = self.get_argument('filename')
		topdf(img)
		self.write(topdf(img))

application = tornado.web.Application([
	(r"/", index)
])

if __name__ == '__main__':
	application.listen(8888)
	tornado.ioloop.IOLoop.instance().start()