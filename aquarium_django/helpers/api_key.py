import secrets


def generate(length: int) -> str:
    """
    Generate API key

    :param length: API key length
    :raises Argument error if length is less than 0
    :returns API key string
    """
    hex = secrets.token_urlsafe(length)
    return str(hex)
