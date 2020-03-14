from sport_hours.extensions import db

class SportActivities(db.Model):
    __tablename__ = 'sport_activities'


    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)

class Clubs(db.Model):
    __tablename__ = 'clubs'

    id = db.Column(db.Integer, db.ForeignKey('sport_activities.id'), primary_key=True)
    leader = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    link = db.Column(db.String(256), nullable=True)
