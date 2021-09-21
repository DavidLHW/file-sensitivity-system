from itsdangerous import TimedJSONWebSignatureSerializer as JsonWebToken
from flask_httpauth import HTTPTokenAuth

# create token.
jwt = JsonWebToken("secret", expires_in=3600)

# Refresh token creation.
refresh_jwt = JsonWebToken("refresh_secret", expires_in=7200)

# Auth object creation.
auth = HTTPTokenAuth("Bearer")