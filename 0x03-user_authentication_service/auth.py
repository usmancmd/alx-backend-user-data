#!/usr/bin/env python3
"""Authentication"""

import bcrypt


def _hash_password(password: str) -> bytes:
    """Hash input password and return the hash"""
    password = password.encode("utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password, salt)
