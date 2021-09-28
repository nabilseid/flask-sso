import socket
import json
import requests
import itertools
from functools import wraps
from flask import request, Response
from .utils import get_config, get_env_from_url


class SsoAuth(object):
    def __init__(self, env=None):
        self.env = env
        self.config = get_config(self.env)
        self.referer = None
        self.sso_response = None

    def validate_ip(self, ip):
        """
        """
        try:
            socket.inet_aton(ip)
            return True
        except socket.error:
            return False

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

        if (self.env == None):
            self.referer = request.headers.get('referer')
            remote_addr = request.environ['REMOTE_ADDR']

            # for local api testing platforms
            if self.referer == None and self.validate_ip(remote_addr):
                self.referer = 'https://localhost:5000'

            self.env = get_env_from_url(self.referer)
            self.config = get_config(self.env)

        self.sso_response = requests.get(
            f'{self.config.ssoURL}/users/me',
            headers={
                'content-type': 'application/json',
                'authorization': request.headers.get('authorization'),
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
            # handle pre-flight request
            if request.method.lower() == 'options':
                return Response()

            if self.authenticate():
                # authentication passed, preced to route function
                return route_func(*args, **kwargs)
            # authenticate failed, return response of sso
            return Response(
                response=self.sso_response.content,
                status=self.sso_response.status_code,
                mimetype='application/json'
            )
        return wrapper

   


    def required_policies(self, serviceactions):
        """
        A decorator factory that would take required service actions as 
        arguments and produces a policy checking decorator to guard a route.

        Example
        -------
        >>> sso_auth = SsoAuth()
        >>> 
        >>> @app.route('/endpoint', methods=['GET'])
        >>> @sso.required_policies(serviceactions=["policy1serviceAction1"])
        >>> def route_func():
        >>>    pass


        """

        def check_policy(route_func,required_serviceactions=serviceactions):
            """
                A decorator to check service actions needed to access a route.
                Gets the required service actions from the decorator factory and 
                checks against users session.

            """

            @wraps(route_func)
            def wrapper(*args, **kwargs):

                    # handle pre-flight request

                if request.method.lower() == 'options':
                    return Response()
                
                self.authenticate()

                # authentication called to get sso content, result can be anything 

                if ( (self.check_user_serviceactions(required_serviceactions) ) | (not self.config.POLICYCHECKTOGGLE) ):

                # policy check toggle is 'ON' and  check has succesfully passed, proceed to route function

                    return route_func(*args, **kwargs)

                # user session doesnt have enough right , return error response

                return Response(response=json.dumps({'data': None,
                                'error': {'message': 'Insufficient rights to  resource'
                                , 'status': 403}}), 
                                status=403,
                                mimetype='application/json') 
                                # "label": "ERR_TOKEN_INVALID"

                

            return wrapper

        return check_policy


    def check_user_serviceactions(self, required_serviceactions):
        """
                check_user_serviceactions

            Return
            ------
            : bool
                true if user is authenticated and has the right service actions other wise false 

            Notes
            -----
            make request to env.sso.adludio.com/users/me with a bearer token
            and once sso content is received proceed to check if user
            has required service actions as part of granted policies 
            else return error with 403 for policy check failure



        """

            # json to python object
        
        sso_response = json.loads(self.sso_response.content.decode('utf-8'))
        
            # proceed to check if required service actions are present
        
        if (sso_response['data'] != None):
            
            # check for reply data from sso 
            
            if 'policies' in sso_response['data']:
                user_serviceactions = [list(x.values())[0] for x in
                                       sso_response['data']['policies']]
                user_serviceactions = \
                    list(itertools.chain(*user_serviceactions))

                    # check required service actions are part of user service actions
                    # also make sure wildcard is granted access

                return set(required_serviceactions).issubset(user_serviceactions) \
                    | ('adl:*:*' in user_serviceactions)

        return False

    
