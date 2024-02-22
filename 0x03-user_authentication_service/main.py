#!/usr/bin/env python3
"""
this module performs integration tests for flask app
"""
import requests
from auth import Auth

EMAIL = ''
BASE_URL = 'http://localhost:5000/'


def register_user(email: str, password: str) -> None:
    '''
    debugging the register user flask route using assert,
    if correct, return none else raise an assertError
    '''
    EMAIL = email
    payload = {
            'email': email,
            'password': password
            }
    resp = requests.post(f'{BASE_URL}users', data=payload)
    assert resp.json() == {"email": email, "message": "user created"}
    assert resp.status_code == 200

    resp = requests.post(f'{BASE_URL}users', data=payload)
    assert resp.json() == {"message": "email already registered"}
    assert resp.status_code == 400


def log_in_wrong_password(email: str, password: str) -> None:
    ''' login in  with the wrong password, this function debugs
        the login view function
    '''
    payload = {
            'email': email,
            'password': password
            }
    resp = requests.post(f'{BASE_URL}sessions', data=payload)
    assert resp.status_code == 401


def log_in(email: str, password: str) -> str:
    '''
    debug the login veiw function with by passing the correct credentials
    '''
    payload = {
            'email': email,
            'password': password
            }
    resp = requests.post(f'{BASE_URL}sessions', data=payload)
    assert resp.status_code == 200
    assert resp.json() == {"email": email, "message": "logged in"}
    token = resp.cookies.get('session_id')
    return token


def profile_unlogged() -> None:
    '''
    debug the profile view function when user not logged in'''
    resp = requests.get(f'{BASE_URL}profile')
    assert resp.status_code == 403


def profile_logged(session_id: str) -> None:
    '''
    debug the profile view functio when the user is logged in
    '''
    cooky = {'session_id': session_id}

    resp = requests.get(f'{BASE_URL}profile', cookies=cooky)
    assert resp.status_code == 200
    assert resp.json() == {"email": EMAIL}


def log_out(session_id: str) -> None:
    '''
    debug the logout view function to alog out as user whow has
    logged in
    '''
    cooky = {'session_id': session_id}
    resp = requests.delete(f'{BASE_URL}sessions', cookies=cooky)
    assert resp.status_code == 200
    assert resp.url == BASE_URL


def reset_password_token(email: str) -> str:
    '''
    debug a reset passord view function
    '''
    payload = {'email': email}
    resp = requests.post(f'{BASE_URL}reset_password', data=payload)
    assert resp.status_code == 200
    token = resp.json().get('reset_token')
    assert resp.json() == {"email": email, "reset_token": token}
    return token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    '''
    debug the view function that updates a password of a user
    '''
    payload = {
            'email': email,
            'reset_token': reset_token,
            'new_password': new_password,
            }
    resp = requests.put(f'{BASE_URL}reset_password', data=payload)
    assert resp.status_code == 200
    assert resp.json() == {"email": email,
                           "message": "Password updated"}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
