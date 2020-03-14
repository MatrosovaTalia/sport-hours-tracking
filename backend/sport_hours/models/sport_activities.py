from sport_hours.extensions import db

class SportActivity(db.Model):
    __tablename__ = 'sport_activity'


    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)

class Club(db.Model):
    __tablename__ = 'club'

    id = db.Column(db.Integer, db.ForeignKey('sport_activity.id'), primary_key=True)
    leader = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    link = db.Column(db.String(256), nullable=True)
