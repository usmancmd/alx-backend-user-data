#!/usr/bin/env python3
"""Authentication"""

import bcrypt
from user import User
from db import DB
from sqlalchemy.orm.exc import NoResultFound
import uuid
from typing import Union


def _hash_password(password: str) -> bytes:
    """Hash input password and return the hash"""
    password = password.encode("utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password, salt)


def _generate_uuid() -> str:
    """Generate and return a string representation of a new UUID"""
    return str(uuid.uuid4())


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

    def valid_login(self, email: str, password: str) -> bool:
        """validate user login"""
        try:
            user = self._db.find_user_by(email=email)
            if user:
                return bcrypt.checkpw(password.encode("utf-8"), user.hashed_password)  # noqa E502
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """Create session for a user and returns the session id"""
        try:
            user = self._db.find_user_by(email=email)
            if user:
                session_id = _generate_uuid()
                self._db.update_user(user.id, session_id=session_id)
                # return session_id
        except NoResultFound:
            return None
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """Get user from session id"""
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            # return user
        except Exception:
            return None

        return user

    def destroy_session(self, user_id: str) -> None:
        """Destroys user session"""
        if user_id is None:
            return None
        return self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """Get reset password token"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError
        reset_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """Update password"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError
        new_password_hash = _hash_password(password)
        try:
            self._db.update_user(user.id, password_hash=new_password_hash, reset_token=None)  # noqa E502
        except Exception:
            raise ValueError
