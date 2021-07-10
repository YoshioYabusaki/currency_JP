import random
import string


def generate_password(password_len: int = 10) -> str:
    if not isinstance(password_len, int):
        raise TypeError('Invalid Type...')

    choices = string.ascii_letters + string.digits + '#$%'
    result = ''

    for _ in range(password_len):
        result += random.choice(choices)

    return result
