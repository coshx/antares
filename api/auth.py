import jwt
from neo4j.v1 import GraphDatabase

DRIVER = GraphDatabase.driver(
    "bolt://localhost:7687", auth=("neo4j", "password"))

def jwtauth(handler_class):
    ''' Handle Tornado JWT Auth '''
    def wrap_execute(handler_execute):
        def require_auth(handler, kwargs):
            token = handler.request.headers._dict['Authorization']
            if token:
                parts = token.split()
                if parts[0].lower() != 'bearer':
                    throw_authorization_error(handler)
                elif len(parts) == 1:
                    throw_authorization_error(handler)
                elif len(parts) > 2:
                    throw_authorization_error(handler)

                jwt_token = parts[1]
                decoded_token =  jwt.decode(jwt_token, handler.settings['jwt_secret'])
                if user_exists(decoded_token['email']):
                    return True
                else:
                    throw_authorization_error(handler)
            else:
                throw_authorization_error(handler)

        def _execute(self, transforms, *args, **kwargs):

            try:
                require_auth(self, kwargs)
            except Exception:
                return False

            return handler_execute(self, transforms, *args, **kwargs)

        return _execute

    handler_class._execute = wrap_execute(handler_class._execute)
    return handler_class

def throw_authorization_error(handler):
    handler._transforms = []
    handler.set_status(401)
    handler.write("invalid header authorization")
    handler.finish()

def user_exists(email):
    with DRIVER.session() as session:
        user = session.write_transaction(
        get_user, email)
        if user:
            return True
        else:
            return False

def get_user(txn, email):
    """Gets user node."""
    query = """
    MATCH (a:User)
    WHERE a.email = "{email}"
    RETURN a
    """.format(email=email)
    result = txn.run(query)
    return result.value()