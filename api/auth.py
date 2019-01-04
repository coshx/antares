"""JWT authenticator decorator for endpoints."""
import json
import jwt
from user_actions import user_exists


def jwt_auth(handler_function):
    """Authenticates JWT against User DB"""

    def _require_auth(self, *args, **kwargs):
        token = self.request.headers.get_list('Authorization').pop()
        if token:
            default_error_msg = "Invalid header authorization"
            parts = token.split()
            if parts[0].lower() != 'bearer':
                throw_authorization_error(self, default_error_msg)
            elif len(parts) == 1:
                throw_authorization_error(self, default_error_msg)
            elif len(parts) > 2:
                throw_authorization_error(self, default_error_msg)

            jwt_token = parts[1]
            try:
                jwt_secret = self.settings['jwt_secret']
                decoded_token = jwt.decode(jwt_token, jwt_secret)
                if user_exists(decoded_token['email']):
                    handler_function(self, *args, **kwargs)
                else:
                    throw_authorization_error(self, default_error_msg)

            except jwt.exceptions.DecodeError as error:
                error_msg = f'Invalid header authorization: {str(error)}'
                throw_authorization_error(self, error_msg)

        else:
            throw_authorization_error(self, default_error_msg)
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
