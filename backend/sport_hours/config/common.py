import os

SECRET_KEY = 'quarantine_sucks' # then replace by os.environ['SECRET_KEY']
SQLALCHEMY_DATABASE_URI = os.environ['DB_URL']
SQLALCHEMY_TRACK_MODIFICATIONS = False
MAX_CONTENT_LENGTH = 16 * 1024 * 1024
