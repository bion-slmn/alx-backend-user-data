#!/usr/bin/env python3
'''
create a session authentication mechanism
'''
from .auth import Auth
import uuid
from models.user import User


class SessionAuth(Auth):
    ''' class to implement session based authN'''
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        '''creates a Session ID for a user_id

        Parameter:
        user_id (str) : the user id passed in the view function

        Return:
        a string which represent the seesion id or None'''
        if not user_id or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        '''retrieving the user id from the  session id provided

        Parameter:
        session_id (str): the session id stored or the user

        Return
        None if no match or return the id'''
        if not session_id or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        '''retrives the current user in the session

        Parameter:
        request (request object): a request passed in th url

        Return:
        a user fron the database or none'''
        # get the user id from the cookie
        if not request:
            return None
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        return User.get(user_id)

    def destroy_session(self, request=None):
        ''' log out a user in a session if the user is preseesnt
        by removing his id in the session

        Parameter:
        request (request object): the request passsed in the url

        return
        True if the user exists int the session or else False'''
        if not request:
            return False
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return False
        self.user_id_by_session_id.pop(session_id)
        return True
