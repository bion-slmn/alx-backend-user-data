#!/usr/bin/env python3
'''this module encypts a password and using bcypt method'''
import bcrypt


def hash_password(password: str) -> str:
    '''function to hash a password

    -Parameter:
    password (str): password to be hashed

    Return:
    a hashed password'''
    bytes_pass = password.encode("utf-8")
    salt = bcrypt.gensalt()

    hashed_pass = bcrypt.hashpw(bytes_pass, salt)
    return hashed_pass


def is_valid(hashed_password: bytes, password: str) -> bool:
    '''check if the password is valid

    Parameter:
    hashed_password (bytes): this is a hashed_password from the database
    password (str): password provided by user

    Return:
    True if the password matches the byte else false'''
    bytes_pass = password.encode("utf-8")

    return bcrypt.checkpw(bytes_pass, hashed_password)
