from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask
from globals import get_app

db = SQLAlchemy(get_app())

class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, db.Sequence('users_id_seq'), primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)

class Instructors(db.Model):
    __tablename__ = 'instructors'

    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)

class SportActivities(db.Model):
    __tablename__ = 'sportactivities'

    id = db.Column(db.Integer, db.Sequence('sportactivities_id_seq'), primary_key=True)
    name = db.Column(db.String, nullable=False)

class Clubs(db.Model):
    __tablename__ = 'clubs'

    id = db.Column(db.Integer, db.ForeignKey('sportactivities.id'), primary_key=True)
    link = db.Column(db.String)

class ClubLeaders(db.Model):
    __tablename__ = 'clubleaders'

    club_id = db.Column(db.Integer, db.ForeignKey('clubs.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

class Admins(db.Model):
    __tablename__ = 'admins'
    __table_args__ = (
        db.PrimaryKeyConstraint('id'),
    )

    id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

class Students(db.Model):
    __tablename__ = 'students'
    __table_args__ = (
        db.PrimaryKeyConstraint('id'),
    )

    id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

class Hours(db.Model):
    __tablename__ = 'hours'
    __table_args__ = (
        db.PrimaryKeyConstraint('date', 'student_id'),
    )

    date = db.Column(db.Date, nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    activity_id = db.Column(db.Integer, db.ForeignKey('sportactivity.id'), nullable=False)
    hours_number = db.Column(db.Integer, db.CheckConstraint('hours_number > 0'))

class ClubParticipants(db.Model):
    __tablename__ = 'clubparticipants'
    __table_args__ = (
        db.PrimaryKeyConstraint('club_id', 'student_id'),
    )

    club_id = db.Column(db.Integer, db.ForeignKey('clubs.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)

class PrimarySportActivities(db.Model):
    __tablename__ = 'primarysportactivities'
    
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), primary_key=True)
    activity_id = db.Column(db.Integer, db.ForeignKey('sportactivities.id'), nullable=False)