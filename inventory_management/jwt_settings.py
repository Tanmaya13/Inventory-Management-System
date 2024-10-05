import secrets

secret_key = secrets.token_urlsafe(64)
JWT_SECRET_KEY = secret_key
JWT_AUTH = {
    'JWT_EXPIRATION_TIME': 60 * 60,  # 1 hour
    'JWT_ALLOW_REFRESH': True,
}