import requests
from functools import wraps
from flask import request, Response
from util import get_config, get_env_from_url

class SsoAuth(object):
    def __init__(self, env = None):
        self.env = env
        self.config = get_config(self.env)
        self.sso_response = None

    def authenticate(self):
        """
        authenticate user 

        Return
        ------
        : bool
            true if user is autherized other wise false 

        Notes
        -----
        make request to env.sso.adludio.com/users/me with a bearer token
            if response is 200, users is authenticated precede to route 
            else return 401 error with sso response content
        """
        
        if (env == None):
            referer = request.headers.get('referer')
            self.env = get_env_from_url(referer)
            self.config = get_config(self.env)

        self.sso_response = requests.get(
            f'{self.config.ssoURL}/users/me',
            headers = {
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
        a decorated to guard a route endpoint

        Example
        -------
        >>> sso_auth = SsoAuth()
        >>> 
        >>> @app.route('/endpoint', methods=['GET'])
        >>> @sso_auth.required
        >>> def route_func():
        >>>    pass
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




