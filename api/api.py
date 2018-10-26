import numpy as np
import tornado.ioloop
import tornado.web

from CSVHandler import CSVHandler
from TreeHandler import TreeHandler

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, worlds")

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/csv", CSVHandler),
        (r"/tree/([^/]+)", TreeHandler),
    ], autoreload = True)

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
