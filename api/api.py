"""Runs loopback server for backend."""
import tornado.ioloop
import tornado.web

from csv_handler import CSVHandler
from tree_handler import TreeHandler


# pylint: disable=W0223
class MainHandler(tornado.web.RequestHandler):
    """Handles smoke tests to localhost:8888/"""

    # pylint: disable=W0221
    def get(self):
        self.write("Hello, worlds")


def make_app():
    """Returns application object for Tornado server."""
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/csv", CSVHandler),
        (r"/tree/([^/]+)", TreeHandler),
    ], autoreload=True)


if __name__ == "__main__":
    APP = make_app()
    APP.listen(8888)
    tornado.ioloop.IOLoop.current().start()
