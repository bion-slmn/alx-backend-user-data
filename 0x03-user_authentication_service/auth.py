#!/usr/bin/env python3
''' module defines a function to encrpyt a password usning bcrypt'''
import bcrypt
from db import DB
from typing import Union
from sqlalchemy.orm.exc import NoResultFound
from user import User
import uuid


def _hash_password(password: str) -> bytes:
    ''' hashes a password

    Parameter:
        password: a string representing a password

    Return:
        bytes : The hashed password.
    '''
    hashpwd = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashpwd


class Auth:
    """Auth class to interact with the authentication database.
            """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str,
                      password: str) -> Union[User, Exception]:
        ''' register a user in the database is doesnt exist or raise exception

        Parameter:
            email (str): a string representing the email of user
            password (str): password of the user

        Return
            a user object or an exception
        '''
        try:
            user = self._db.find_user_by(email=email)
            if user:
                raise ValueError(f'User {email} already exists')
        except NoResultFound:
            user = self._db.add_user(email, _hash_password(password))
            return user

    def valid_login(self, email: str, password: str) -> bool:
        '''validate the user by email if exists in the database
        and also confirm that the password match with that in the databse

        paramete:
            email (str): a string representing the email of user
            password (str): password of the user

        ReturnL
            True if details match that in the databse else Falsie'''

        try:
            user = self._db.find_user_by(email=email)
            hashed_pwd = user.hashed_password
            return bcrypt.checkpw(password.encode('utf-8'), hashed_pwd)
        except NoResultFound:
            return False

    def _generate_uuid(self) -> str:
        '''generate a uuid string

        Return:
            a uuid string represenataion'''

        return str(uuid.uuid4())

    def create_session(self, email: str) -> str:
        '''finds a user with the corresponding email address in the database,
        create a seesion id for the user and stores in the
        database as th session id

        Parameter:
            email:  email of the user

        Return:
             the session id of the user or nothing if no user '''
        try:
            user = self._db.find_user_by(email=email)
            s_id = self._generate_uuid()
            self._db.update_user(user.id, session_id=s_id)
            return s_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[None, User]:
        '''
        get a user from the database who match session id provided
        and return the user or none

        Parameter:
            session_id: a string representing the session id

        Return:
            a user or none
        '''
        try:
            user = self._db.find_user_by(session_id=session_id)

            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        '''get user with matching user id and update the session_id
        to none

        Parmater:
            user_id: integer representing the id of the user
        '''
        user = self._db.find_user_by(id=user_id)
        self._db.update_user(user.id, session_id=None)
        return None

    def get_reset_password_token(self, email: str) -> str:
        '''
        generates a token that is used to reset password,

        Parameters:
            email (str): email of the user

        Return:
            a uuid str or a value error if that email doesnt exist
            in the database
        '''
        try:
            user = self._db.find_user_by(email=email)
            token = self._generate_uuid()
            self._db.update_user(user.id, reset_token=token)
            return token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        '''
        update the password of a user

        Parameter:
            reset_token: a string to represent reset token of the user
            password: new password passed by the user

        '''
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hash_password = _hash_password(password)
            self._db.update_user(user.id, hashed_password=hash_password)
            self._db.update_user(user.id, reset_token=None)
        except NoResultFound:
            raise ValueError
