import os
from app.utils import generate_secure_random_string

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or  generate_secure_random_string(16)
    
    DEBUG = True
    
    CACHE_TYPE = 'SimpleCache'  # Use 'RedisCache' or 'MemcachedCache' for production
    CACHE_DEFAULT_TIMEOUT = 300

