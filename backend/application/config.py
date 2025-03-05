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