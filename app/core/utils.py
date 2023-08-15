import random
import string

VALUE_FOR_RANDOMIZER: int = 10
USER_PASSWORD_LEN: int = 3


def generate_unique_id():
    all_chars = string.ascii_letters + string.digits
    return ''.join(
        random.choice(all_chars) for _ in range(VALUE_FOR_RANDOMIZER)
    )
