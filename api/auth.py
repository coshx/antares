import jwt
import json
from user_actions import user_exists


def jwt_auth(handler_function):
    '''Authenticates JWT against User DB'''

    def _require_auth(self, *args, **kwargs):
        token = self.request.headers._dict['Authorization']
        if token:
            parts = token.split()
            if parts[0].lower() != 'bearer':
                throw_authorization_error(self)
            elif len(parts) == 1:
                throw_authorization_error(self)
            elif len(parts) > 2:
                throw_authorization_error(self)

            jwt_token = parts[1]
            decoded_token = jwt.decode(jwt_token, self.settings['jwt_secret'])
            if user_exists(decoded_token['email']):
                handler_function(self, *args, **kwargs)
            else:
                throw_authorization_error(self)
        else:
            throw_authorization_error(self)
    return _require_auth


def throw_authorization_error(handler):
    handler._transforms = []
    handler.set_status(401)
    handler.write("Invalid header authorization")
    handler.finish(json.dumps({
        'error': {
            'code': 401,
            'message': "Invalid header authorization",
        }
    }))
