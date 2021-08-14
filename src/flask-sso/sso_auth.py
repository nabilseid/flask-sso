import requests
from functools import wraps
from flask import request, Response
from util import get_config, get_env_from_url

class SsoAuth(object):
    def __init__(self):
        self.sso_response = None

    def authenticate(self):
        """
        """
        
        referer = request.headers.get('referer')
        env = get_env_from_url(referer)
        config = get_config(env)

        self.sso_response = requests.get(
            f'{config.ssoURL}/users/me',
            headers={
                'content-type':'application/json',
                'authorization':request.headers.get('authorization'),
                'Access-Origin': '*'
            }
        )

        if self.sso_response.status_code == 200:
            return True

        return False

    def required(self, route_func):
        """
        """

        @wraps(route_func)
        def wrapper(*args, **kwargs):
            if self.authenticate():
                # authentication passed, preced to route function
                return route_func(*args, **kwargs)
            # authenticate failed, return response of sso 
            return Response(
                response = self.sso_response.content,
                status = self.sso_response.status_code,
                mimetype = 'application/json'
            )




