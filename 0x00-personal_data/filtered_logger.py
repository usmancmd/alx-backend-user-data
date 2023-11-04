#!/usr/bin/env python3
"""filter_datum that returns the log message obfuscated"""

import re


def filter_datum(fields, redaction, message, separator):
    """returns the log message obfuscated"""
    pwrd = r'(?<=password=)[a-z]+'
    date = r'(?<=date_of_birth=)\d{2}/\d{2}/\d{4}'
    message = re.sub(pwrd, redaction, re.sub(date, redaction, message))
    return message
