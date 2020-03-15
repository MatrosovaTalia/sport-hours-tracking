from sport_hours.extensions import db
from sqlalchemy.dialects import postgresql


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    roles = db.Column(postgresql.ARRAY(db.String(32)), nullable=False)
    # property `activities` available with a backref
