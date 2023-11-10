#!/usr/bin/env python3
"""Class Auth to manage the API authentication"""

from flask import request
from typing import List, TypeVar
import os


class Auth():
    """Auth class"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """require_auth method"""
        if path is None or excluded_paths is None or excluded_paths == []:
            return True

        if len(path) == 14:
            path = f"{path}/"

        if path in excluded_paths:
            return False

        for ex_path in excluded_paths:
            if ex_path.startswith(path):
                return False
            elif path.startswith(ex_path):
                return False
            if ex_path[-1] == "*":
                if path.startswith(ex_path[:-1]):
                    return False

        return True

    def authorization_header(self, request=None) -> str:
        """authorization_header method"""
        if request is None or "Authorization" not in request.headers:
            return None
        else:
            return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """current_user"""
        return None

    def session_cookie(self, request=None):
        """Returns a cookie value from a request"""
        if request is None:
            return None
        cookie_name = os.getenv("SESSION_NAME")
        return request.cookies.get(cookie_name)
