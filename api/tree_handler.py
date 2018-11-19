"""Handles requests to retrieve and evaluate decision trees."""
import tornado.web


# pylint: disable=W0223
class TreeHandler(tornado.web.RequestHandler):
    """Handles all CRUD operations on decision trees."""

    # pylint: disable=W0221
    def get(self, slug):
        """Retrieves decison tree based on ID."""
        # tree = self.db.get("SELECT * FROM entries WHERE slug = %s", slug)
        # if not entry: raise tornado.web.HTTPError(404)
        self.write(slug)

    # pylint: disable=W0221
    def post(self):
        """Classifies input instance using decision tree ID."""
        test_data = self.get_argument("data")
        self.write(test_data)
