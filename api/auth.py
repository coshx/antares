"""JWT authenticator decorator for endpoints."""
import json
import jwt
from user_actions import user_exists


def jwt_auth(handler_function):
    """Authenticates JWT against User DB"""

    def _require_auth(self, *args, **kwargs):
        token = self.request.headers.get_list('Authorization').pop()
        if token:
            parts = token.split()
            if parts[0].lower() != 'bearer':
                throw_authorization_error(self, "Invalid header authorization")
            elif len(parts) == 1:
                throw_authorization_error(self, "Invalid header authorization")
            elif len(parts) > 2:
                throw_authorization_error(self, "Invalid header authorization")

            jwt_token = parts[1]
            try:
                decoded_token = jwt.decode(jwt_token, self.settings['jwt_secret'])
                if user_exists(decoded_token['email']):
                    handler_function(self, *args, **kwargs)
                else:
                    throw_authorization_error(self, "Invalid header authorization")

            except jwt.exceptions.DecodeError as error:
                error_msg = f'Invalid header authorization: {str(error)}'
                throw_authorization_error(self, error_msg)

        else:
            throw_authorization_error(self, "Invalid header authorization")
    return _require_auth


def throw_authorization_error(handler, error_msg):
    """Responds to invalid request with error"""
    handler.set_status(401)
    handler.finish(json.dumps({
        'error': {
            'code': 401,
            'message': error_msg,
        }
    }))
