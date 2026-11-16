import random
import string


def make_cipher() -> tuple[dict, dict]:
    chars = list(string.ascii_letters + string.digits)
    shuffled = random.sample(chars, len(chars))
    encoder = dict(zip(chars, shuffled))
    decoder = {v: k for k, v in encoder.items()}
    return encoder, decoder


def apply_mapping(text: str, mapping: dict) -> str:
    return ''.join(mapping.get(c, c) for c in text)
