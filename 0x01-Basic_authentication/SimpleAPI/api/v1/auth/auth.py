#!/usr/bin/env python3
'''this module create a class that manages API authentication'''
from flask import request
from typing import TypeVar, List


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

        if path == None:
            return True
        if excluded_paths == None or not excluded_paths:
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
        if request == None:
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
