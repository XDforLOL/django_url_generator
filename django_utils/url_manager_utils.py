from datetime import datetime
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
import base64
import hashlib

def is_valid_url(url: str) -> bool:
    validate = URLValidator()
    try:
        validate(url)
        return True
    except ValidationError:
        return False

def url_hasher(long_url: str) -> str:
    # I am using the current datetime to make the hash unique,
    # and then I am encoding the hash with base64 to make it shorter
    # this was designed with a user system in mind so that the same user
    # can have the same short url for the same long url so with that in mind
    # I would hash it with a last login datetime with the long url
    hash_object = hashlib.md5((long_url + datetime.now().isoformat()).encode())
    hash_digest = hash_object.digest()
    return base64.urlsafe_b64encode(hash_digest).decode()[:6]