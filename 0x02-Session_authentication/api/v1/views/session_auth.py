#!/usr/bin/env python3
''' modules defines view function for session authN'''
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_login():
    '''view function to retrive the login details of the user'''
    email = request.form.get('email')
    password = request.form.get('password')
    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400

    user_list = User.search({'email': email})
    if not user_list:
        return jsonify({"error": "no user found for this email"}), 404
    for user in user_list:
        if user.is_valid_password(password):
            from api.v1.app import auth
            user_id = user.id
            session_id = auth.create_session(user_id)
            session_name = os.getenv('SESSION_NAME')
            response = jsonify(user.to_json())
            response.set_cookie(session_name, session_id)
            return response
    return jsonify({"error": "wrong password"})


@app_views.route('auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def sesion_logout():
    '''log out a user from a session and delete the session id'''
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({})
    abort(404)
