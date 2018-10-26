import tornado.ioloop
import tornado.web

#import pdb; pdb.set_trace()
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, worlds")

class CSVHandler(tornado.web.RequestHandler):
    def post(self):
        data = self.get_argument("csv")
        self.write(data) 

class TreeHandler(tornado.web.RequestHandler):
    #get tree ID, return complexity level, accuracy against training model
    def get(self, slug):
        # tree = self.db.get("SELECT * FROM entries WHERE slug = %s", slug)
        # if not entry: raise tornado.web.HTTPError(404)
        self.write(slug)

    #classify tree ID - run with test data, return classification and explanation
    def post(self, slug):
        test_data = self.get_argument("data")
        self.write(test_data)
        
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
