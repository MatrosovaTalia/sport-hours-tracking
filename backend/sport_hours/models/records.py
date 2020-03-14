from sport_hours.extensions import db

class SportHours(db.Model):
    __tablename__ = 'sport_hours'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    name = db.Column(db.String(128), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    activity_id = db.Column(db.Integer, db.ForeignKey('sport_activity.id'), nullable=False)
    hours_number = db.Column(db.Integer, db.CheckConstraint('hours_number > 0'))


class ActivityAssignment(db.Model):
    __tablename__ = 'activity_assignment'
    __table_args__ = (db.PrimaryKeyConstraint('student_id', 'activity_id'),)


    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    activity_id = db.Column(db.Integer, db.ForeignKey('sport_activity.id'), nullable=False)
