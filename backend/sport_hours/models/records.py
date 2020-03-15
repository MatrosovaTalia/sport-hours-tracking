from sport_hours.extensions import db

class SportHoursRecords(db.Model):
    __tablename__ = 'sport_hours_records'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    activity_id = db.Column(db.Integer, db.ForeignKey('sport_activity.id'), nullable=False)
    hours_number = db.Column(db.Integer, db.CheckConstraint('hours_number > 0'))


class ActivityAssignments(db.Model):
    __tablename__ = 'activity_assignments'
    __table_args__ = (db.PrimaryKeyConstraint('student_id', 'activity_id'),)

    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    activity_id = db.Column(db.Integer, db.ForeignKey('sport_activities.id'), nullable=False)
