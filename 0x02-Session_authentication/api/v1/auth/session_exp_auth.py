#!/usr/bin/env python3
''' module defines a a class for sesssion based authN that expires'''
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
import os


class SessionExpAuth(SessionAuth):
    ''' defines an session based AuthN that has an expirey date'''

    def __init__(self):
        duration = os.getenv('SESSION_DURATION ')
        try:
            duraation = int(duration)
        except Exception:
            duration = 0
        self.session_duration = duration

    def create_session(self, user_id=None):
        '''create a session id by calling the parent class

        Parameter:
        user_id (str): the id of the user a uuid4 str

        Return:
        a session_id or None'''
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        session_dictionary = {
                            'user_id': user_id,
                            'created_at': datetime.now()
                            }
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        '''retrieving the user id from the  session id provided

        Parameter:
        session_id (str): the session id stored or the user
        Return
        None if no match or return the id'''
        id_session = self.user_id_by_session_id.get(session_id)
        if not session_id or not id_session:
            return None
        if self.session_duration <= 0:
            return id_session.get('user_id')
        if not id_session.get('created_at'):
            return None
        created_at = id_session.get("created_at")
        allowed_window = created_at + timedelta(seconds=self.session_duration)
        if allowed_window < datetime.now():
            return None
        return id_session.get('user_id')
