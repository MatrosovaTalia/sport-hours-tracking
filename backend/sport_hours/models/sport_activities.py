from sport_hours.extensions import db


activity_assignment = db.Table(
    'activity_assignment',
    db.Column('activity_id', db.Integer,
              db.ForeignKey('sport_activities.id', ondelete='CASCADE'),
              primary_key=True),
    db.Column('student_email', db.String(128),
              db.ForeignKey('users.email', ondelete='CASCADE'),
              primary_key=True)
)


class SportActivity(db.Model):
    __tablename__ = 'sport_activities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    assigned_students = db.relationship('User',
                                        secondary=activity_assignment,
                                        lazy=True,
                                        backref=db.backref('activities', lazy=True))

    schedule_records = db.relationship('ActivityScheduleRecord')


class Club(db.Model):
    __tablename__ = 'clubs'

    id = db.Column(db.Integer, db.ForeignKey('sport_activities.id'), primary_key=True)
    leader = db.Column(db.String(128), db.ForeignKey('users.email'), nullable=False)
    link = db.Column(db.String(256), nullable=True)


class ActivityScheduleRecord(db.Model):
    __tablename__ = 'activity_schedule'

    id = db.Column(db.Integer, primary_key=True)
    activity = db.Column(db.Integer,
                         db.ForeignKey('sport_activities.id', ondelete='CASCADE'),
                         nullable=False)
    day = db.Column(db.Integer, db.CheckConstraint('0 <= day AND day <= 6'), nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    finish_time = db.Column(db.Time, db.CheckConstraint('finish_time > start_time'), nullable=False)
    location = db.Column(db.String(64), nullable=False)
