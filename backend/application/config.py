class Config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///lms.sqlite3'
    SECRET_KEY = 'secretkey'
    SECURITY_PASSWORD_SALT = 'saltsalt'
    WTF_CSRF_ENABLED = False
    # Flask-User configuration
    SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authentication-Token'
    # SECURITY_TOKEN_MAX_AGE = 3600
    SECURITY_LOGIN_WITHOUT_CONFIRMATION = True
    # cache configuration
    CACHE_TYPE = 'RedisCache'
    CACHE_REDIS_HOST = 'localhost'
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_DB = 0
    CACHE_REDIS_URL = 'redis://localhost:6379/0'
    CACHE_DEFAULT_TIMEOUT = 300