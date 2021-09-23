from itsdangerous import TimedJSONWebSignatureSerializer as JsonWebToken
from flask_httpauth import HTTPTokenAuth

import hashlib

# create token.
jwt = JsonWebToken("secret", expires_in=3600)

# Refresh token creation.
refresh_jwt = JsonWebToken("refresh_secret", expires_in=7200)

# Auth object creation.
auth = HTTPTokenAuth("Bearer")


def generate_password_hash(password):
    """
    Return a SHA-256 hash of the given password
    """
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


def check_password_hash(hash_to_compare, password):
    """
    Return a True if hash matches hashed password
    """
    password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    return True if password_hash == hash_to_compare else False