import re


def sanitize(string):
    sanitized = string.replace(" ", "_")
    sanitized = re.sub(r"[^\w\d._-]", "", sanitized)
    sanitized = sanitized.lower()
    return sanitized
