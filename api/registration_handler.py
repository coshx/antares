"""Handles user node creation and retrieval"""
import json
import jwt
import tornado.web
from neo4j.v1 import GraphDatabase
from bcrypt import hashpw, gensalt
from user_actions import get_user, create_user, user_exists

DRIVER = GraphDatabase.driver(
    "bolt://localhost:11001", auth=("neo4j", "password"))

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
        body = json.loads(self.request.body.decode('utf-8'))
        email = body['email']
        password = body['password']

        if not user_exists(email):
            utf8_pw = password.encode('utf-8')
            hashed_pw = hashpw(utf8_pw, gensalt()).decode('utf-8')
            with DRIVER.session() as session:
                if session.write_transaction(
                        create_user, email, hashed_pw):
                    session_token = jwt.encode({'email': email},
                                               self.settings['jwt_secret'],
                                               algorithm='HS256')
                    self.write(json.dumps({
                        "session_token": session_token.decode('utf-8')
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

        hashedpw_utf8 = hashed_pw.encode('utf-8')
        pw_utf8 = password.encode('utf-8')
        if not user:
            error_message = "No user with that email and password " \
                "combination exists!"
        elif hashpw(pw_utf8, hashedpw_utf8) == hashedpw_utf8:
            session_token = jwt.encode({'email': email},
                                       self.settings['jwt_secret'],
                                       algorithm='HS256')
            return self.finish(json.dumps({
                "session_token": session_token.decode('utf-8')
            }))
        else:
            error_message = "Incorrect password"

        self.set_status(400)
        return self.finish(json.dumps({
            'error': {
                'code': 400,
                'message': error_message,
            }
        }))

    def options(self):
        self.set_header("Allow", "POST, GET, OPTIONS")
        self.set_status(200)
        self.finish()
