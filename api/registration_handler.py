"""Handles user node creation and retrieval"""
import json
import tornado.web
from neo4j.v1 import GraphDatabase
from bcrypt import hashpw, gensalt

DRIVER = GraphDatabase.driver(
    "bolt://localhost:7687", auth=("neo4j", "password"))

# pylint: disable=W0223


class RegistrationHandler(tornado.web.RequestHandler):
    """Handles all CRUD operations on Registrations."""

    # pylint: disable=W0221
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def post(self):
        """Checks if user exists if not, creates new user."""
        email = self.get_query_argument('email')
        password = self.get_query_argument('password')
        new_user = ""
        with DRIVER.session() as session:
            user_exists = session.write_transaction(
                get_user, email)
            if not user_exists:
                hashed_pw = hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')
                new_user = session.write_transaction(
                    create_user, email, hashed_pw)
        if new_user != "":
            self.write(json.dumps({
                "email": email,
                "password": hashed_pw
            }))
        else:
            self.set_status(400)
            self.finish(json.dumps({
                'error': {
                    'code': 400,
                    'message': "A user with that email already exists!",
                }
            }))

    def get(self):
        """Gets exising user and signs them in"""
        email = self.get_query_argument('email')
        password = self.get_query_argument('password')
        error_message = ""
        with DRIVER.session() as session:
            user = session.write_transaction(
                get_user, email)
            hashed_pw = user[0].get("password")
        if not user:
            error_message = """No user with that email and password
                                combination exists!"""
        elif hashpw(password.encode('utf-8'), hashed_pw.encode('utf-8')) == hashed_pw.encode('utf-8'):
            return self.finish(json.dumps({
                "email": user[0].get("email"),
                "password": hashed_pw
            }))
        else:
            error_message = "Incorrect password"
        
        self.set_status(400)
        self.finish(json.dumps({
            'error': {
                'code': 400,
                'message': error_message,
            }
        }))

    def options(self):
        # no body
        self.set_status(204)
        self.finish()


def get_user(txn, email):
    """Gets user node."""
    query = """
    MATCH (a:User)
    WHERE a.email = "{email}"
    RETURN a
    """.format(email=email)
    result = txn.run(query)
    return result.value()


def create_user(txn, email, password):
    """Creates a user node."""
    query = """
    MERGE (a:User {email: $email,
                password: $password})
    """
    return txn.run(
        query,
        email=email,
        password=password)
