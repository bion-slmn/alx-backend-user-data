#!/usr/bin/env python3
'''
Creeate a classs Basic Auth that inherits from auth class
'''
from api.v1.auth.auth import Auth
from typing import TypeVar
from models.user import User
import base64


class BasicAuth(Auth):
    '''creates a basic auth class'''
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        '''extracts base64 authorization header
        and returns base64 part of the header'''

        if not authorization_header \
                or not isinstance(authorization_header, str) \
                or not authorization_header.startswith('Basic '):
            return None
        base64_part = authorization_header.split(' ', 1)[1]
        return base64_part

    def decode_base64_authorization_header(
                                           self,
                                           base64_authorization_header: str
                                           ) -> str:
        '''decode base64 part back to a string
            Returns a string fron the authorizatio header
        '''
        try:
            if not base64_authorization_header \
                    or not isinstance(base64_authorization_header, str):
                return None
            decoded_bytes = base64.b64decode(base64_authorization_header)
            header_str = decoded_bytes.decode('utf-8')
            return header_str
        except Exception as e:
            return None

    def extract_user_credentials(
                                 self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        ''' extract the user credentials from the decoded auth header
        Return the email and password'''
        if not decoded_base64_authorization_header \
                or not isinstance(decoded_base64_authorization_header, str) \
                or ':' not in decoded_base64_authorization_header:
            return (None, None)
        return tuple(decoded_base64_authorization_header.split(':', 1))

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        '''obtains a user instance baseed on the emails provided'''
        if not user_email or not isinstance(user_email, str):
            return None
        if not user_pwd or not isinstance(user_pwd, str):
            return None

        details = {
                'email': user_email,
                }
        user_list = User.search(details)
        if user_list:
            for user in user_list:
                if user.is_valid_password(user_pwd):
                    return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        '''get the current user fron the values passed in the authorization
        header'''
        auth_header = self.authorization_header(request)

        base_64 = self.extract_base64_authorization_header(auth_header)
        decoded_auth = self.decode_base64_authorization_header(base_64)
        details = self.extract_user_credentials(decoded_auth)
        user = self.user_object_from_credentials(*details)

        return user
