#!/usr/bin/env python3
'''this module create a class that manages API authentication'''
from typing import TypeVar, List
from flask import request
import os


class Auth:
    '''class to handle API authentication '''
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        '''
        function check if a path requires authentication
        Parameter:
        path (str): a path to api resources
        excluded_path (list of strings): a lisat of path that are exluded

        Return:
        a boolean
        '''

        if not path:
            return True
        if excluded_paths is None or not excluded_paths:
            return True
        #  allowing * at the end on excluded paths
        for route in excluded_paths:
            if route.endswith('*') and path.startswith(route[:-1]):
                return False
        if not path.endswith('/'):
            path += '/'
        if path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        '''
        get the authorization header from the request object
        Parameter:
        request (flask object): the request passed by the user
        Return
        None or the content of the authorisation header
        '''
        if request is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        '''
        get the current user
        Parameter
        request (flask object)
        Return
        None
        '''
        return None

    def session_cookie(self, request=None):
        '''returns a cookie value from a request

        Parameter:
        request (request object):

        Return
        the value of the cookie whose key is passed inthe
        environmental variable'''
        if not request:
            return None
        _my_session_id = os.getenv('SESSION_NAME')
        return request.cookies.get(_my_session_id)
