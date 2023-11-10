#!/usr/bin/env python3
"""SessionAuth Authentication Class"""

from api.v1.auth.auth import Auth
import uuid

class SessionAuth(Auth):
    """SessionAuth Class"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Create session by user id"""
        if user_id is None:
            return None
        if type(user_id) is not str:
            return None
        session_id = uuid.uuid4()
        SessionAuth.user_id_by_session_id[session_id] = user_id
        return session_id

