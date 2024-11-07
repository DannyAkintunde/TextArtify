import os
import secrets

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or  secrets.token_hex(16)
    
    DEBUG = True
    
    CACHE_TYPE = 'SimpleCache'  # Use 'RedisCache' or 'MemcachedCache' for production
    CACHE_DEFAULT_TIMEOUT = 300

