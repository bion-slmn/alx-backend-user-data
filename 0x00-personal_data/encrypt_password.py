#!/usr/bin/env python3
'''this module encypts a password and using bcypt method'''
import bcrypt


def hash_password(password: str) -> str:
    '''function to hash a password adn return a hashed byte string'''
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    '''check if the password is valid'''

    return bcrypt.checkpw(password.encode("utf-8"), hashed_password)
