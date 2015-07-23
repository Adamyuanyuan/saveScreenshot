#-*-coding:utf8-*-

import web
web.__file__
urls = (
	'/','index'
)

class index:
	def GET(self):
		print "hello, world!"

if __name__ == "__main__":
	web.run(urls,globals())