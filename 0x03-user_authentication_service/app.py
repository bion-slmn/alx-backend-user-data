#!/usr/bin/env python3
'''module to define a flask app and routes for flask view function'''
from flask import Flask, jsonify, Response, request, abort, redirect, url_for
from auth import Auth
from typing import Union


AUTH = Auth()
app = Flask(__name__)


@app.route('/')
def home() -> Response:
    ''' view function for the home route

    Return
        Response: A JSON response containing a dictionary.
    '''
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def register_user() -> Response:
    ''' regisater a user to the database from the information given from the
    form. If the user exists no registration to the database

    Return:
        REsponse: a json response with a message indicating if the user exists
    '''
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        a_user = AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login() -> Response:
    '''
    login a user if exists in the database

    or raise unauthorised error 401
    '''
    email = request.form.get('email')
    password = request.form.get('password')

    if AUTH.valid_login(email, password):
        s_id = AUTH.create_session(email)
        resp = jsonify({"email": email, "message": "logged in"})
        resp.set_cookie("session_id", s_id)
        return resp

    abort(401)


@app.route('/sessions', methods=['DELETE'])
def logout() -> Response:
    '''
    log out a user if exits else raise 403 ecxeption

    and redirect to the home page
    '''
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect(url_for('home'))
    abort(403)


@app.route('/profile')
def profile() -> Response:
    '''get a user if exists from the sesiion id in the cookie
    and return the users email or exeption if not exits
    '''
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email})
    abort(403)


@app.route('/reset_password', methods=['POST'])
def reset_password():
    '''
    reset  a password by providing a areset token if the user email
    provide in the form

    return a json format
    '''
    email = request.form.get('email')

    try:
        token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": token})
    except ValueError:
        abort(403)


@app.route('/reset_password', methods=['PUT'])
def update_password():
    '''update the password of the user by reading the content o fthe
    form.
    '''
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": new_password})
    except ValueError as e:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
