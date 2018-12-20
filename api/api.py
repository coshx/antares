"""Runs loopback server for backend."""
import tornado.ioloop
import tornado.web

from csv_handler import CSVHandler
from tree_handler import TreeHandler
from registration_handler import RegistrationHandler


# pylint: disable=W0223
class BaseHandler(tornado.web.RequestHandler):
    """Sets session token to track current user"""
    def get_current_user(self):
        return self.get_secure_cookie("user")


class MainHandler(BaseHandler):
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
        (r"/registration", RegistrationHandler)
    ], autoreload=True, cookie_secret="123457788")


if __name__ == "__main__":
    APP = make_app()
    APP.listen(8888)
    tornado.ioloop.IOLoop.current().start()
