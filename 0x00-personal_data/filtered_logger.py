#!/usr/bin/env python3
"""filter_datum that returns the log message obfuscated"""

import re


def filter_datum(fields: str,
                 redaction: str,
                 message: str,
                 separator: str) -> str:
    """returns the log message obfuscated"""
    pw = r'(?<=password=)[a-z]+'
    dt = r'(?<=date_of_birth=)\d{2}/\d{2}/\d{4}'
    return re.sub(pw, redaction, re.sub(dt, redaction, message))
