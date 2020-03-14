import os


SQLALCHEMY_DATABASE_URI = 'postgresql://natalia:holyshit@localhost:5433/sport_hours'
# SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SQLALCHEMY_TRACK_MODIFICATIONS = False
MAX_CONTENT_LENGTH = 16 * 1024 * 1024