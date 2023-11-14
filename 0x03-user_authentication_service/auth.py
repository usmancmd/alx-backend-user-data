#!/usr/bin/env python3
"""Authentication"""

import bcrypt
from user import User
from db import DB
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """Hash input password and return the hash"""
    password = password.encode("utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password, salt)


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register user"""
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            password_hash = _hash_password(password)
            return self._db.add_user(email, password_hash)
        raise ValueError(f"User {email} already exists")
