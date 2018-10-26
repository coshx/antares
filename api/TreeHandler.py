import sklearn.tree
import tornado.web


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
