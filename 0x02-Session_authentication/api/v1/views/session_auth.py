#!/usr/bin/env python3
"""
Flask view that handles all routes for the Session authentication
"""
from flask import request, jsonify, abort
from api.v1.views import app_views
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """session auth"""
    email = request.form.get("email")
    password = request.form.get("password")
    if email is None or email == '':
        return jsonify({"error": "email missing"}), 400
    if password is None or password == '':
        return jsonify({"error": "password missing"}), 400
    users = User.search({"email": email})
    if users is None or len(users) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    if users[0].is_valid_password(password):
        from api.v1.app import auth
        session_id = auth.create_session(users[0].id)
        user_json = jsonify(users[0].to_json())
        session_name = os.getenv("SESSION_NAME")
        user_json.set_cookie(session_name, session_id)
        return user_json
    return jsonify({"error": "wrong password"}), 401


@app_views.route('auth_session/logout', methods=['DELETE'], strict_slashes=False)  # noqa E502
def logout():
    """logout user"""
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200
