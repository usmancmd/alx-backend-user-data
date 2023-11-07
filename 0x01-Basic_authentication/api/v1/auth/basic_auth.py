#!/usr/bin/env python3
"""Basic Auth class"""

from api.v1.auth.auth import Auth
import base64


class BasicAuth(Auth):
    """BasicAuth class"""
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """extract_base64_authorization_header method"""
        if authorization_header is None:
            return None
        if type(authorization_header) is not str:
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """decode_base64_authorization_header method"""
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) is not str:
            return None
        try:
            decoded_value = base64.b64decode(base64_authorization_header)
        except base64.binascii.Error:
            return None

        return decoded_value.decode('utf-8')

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """"extract_user_credentials method"""
        if decoded_base64_authorization_header is None:
            return (None, None)
        if type(decoded_base64_authorization_header) is not str:
            return (None, None)
        if ":" not in decoded_base64_authorization_header:
            return (None, None)
        user_email, password = decoded_base64_authorization_header.split(":")
        return (user_email, password)
