import uuid


def get_formatted_uuid() -> str:
    """
    It generates a random UUID and returns it in uppercase hexadecimal format
    return: A random string of hexadecimal characters.
    """
    return uuid.uuid4().hex.upper()
