from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from globals import app

password = input("Input password for user postgres:")
engine = create_engine(f'postgresql://postgres:{password}@localhost:5432/sport', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                        autoflush=False,
                                        bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://postgres:{password}@localhost:5432/sport"

from models import Users, Instructors, SportActivities, Clubs, ClubLeaders, Admins, Students, Hours, ClubParticipants, PrimarySportActivities

@app.route('/')
def hello():
    h = Hours.query.first()
    return str(h.hours_number)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == '__main__':
    app.run()