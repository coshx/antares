"""Runs loopback server for backend."""
import configparser
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
        import pdb; pdb.set_trace()
        if not self.get_secure_cookie("mycookie"):
            self.set_secure_cookie("mycookie", "myvalue")
            self.write("Your cookie was not set yet!")
        else:
            self.write("Your cookie was set!")



def make_app():
    """Returns application object for Tornado server."""
    config = configparser.ConfigParser()
    config.read('config.ini')
    cookie_secret = config['DEFAULT']['COOKIE_SECRET_KEY']
    jwt_secret = config['DEFAULT']['JWT_SECRET_KEY']
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/csv", CSVHandler),
        (r"/tree/([^/]+)", TreeHandler),
        (r"/registration", RegistrationHandler)],
                                   autoreload=True,
                                   cookie_secret=cookie_secret,
                                   jwt_secret=jwt_secret)


if __name__ == "__main__":
    APP = make_app()
    APP.listen(8888)
    tornado.ioloop.IOLoop.current().start()
