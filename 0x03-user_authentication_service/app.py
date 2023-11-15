#!/usr/bin/env python3
"""Flask app"""

from flask import Flask, jsonify, request, abort
from sqlalchemy.orm.exc import NoResultFound
from auth import Auth

AUTH = Auth()
app = Flask(__name__)


@app.route("/")
def index():
    """index page endpoint"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def users():
    """Register new user"""
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": f"{email}", "message": "user created"})  # noqa E502
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"])
def login():
    """Login user"""
    email = request.form.get("email")
    password = request.form.get("password")

    if not AUTH.valid_login(email, password):
        abort(401)

    session_id = AUTH.create_session(email)
    response = jsonify({"email": f"{email}", "message": "logged in"})
    response.set_cookie("session_id", session_id)
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
