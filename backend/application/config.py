from flask import current_app as app
from flask_caching import Cache
import sqlite3

class Config():
  DEBUG = False
  SQLALCHEMY_TRACK_MODIFICATIONS = True

class LocalDevelopmentConfig(Config):
  # configuration
  DEBUG = True
  SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite3"

  # configuration for security
  SECRET_KEY = "6fcf1f70837d113620f7e448d7656ab71b3fa8cd52a7efed1f6bf2ee0a54efab" # it helps to hash user credentials in session
  SECURITY_PASSWORD_HASH = "bcrypt" # mechanism for password hashing
  SECURITY_PASSWORD_SALT = "H_CyLZHSE6yGHgnb3Mgq1g" # it helps to hash passwords
  WTF_CSRF_ENABLED = False # it helps to disable cross-site request forgery

  # configuration for authentication
  SECURITY_TOKEN_AUTHENTICATION_HEADER = "Authentication-Token"
  # configuration for caching
  CACHE_TYPE = "RedisCache"
  CACHE_REDIS_HOST = "localhost"
  CACHE_REDIS_PORT = 6379
  # CACHE_REDIS_DB = 0
  CACHE_DEFAULT_TIMEOUT = 300

