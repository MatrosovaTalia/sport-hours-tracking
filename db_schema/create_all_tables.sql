CREATE TABLE Users (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR NOT NULL,
    last_name VARCHAR NOT NULL
);

CREATE TABLE Instructors (
    id INTEGER REFERENCES Users(id) PRIMARY KEY
);

CREATE TABLE SportActivities (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL
);

CREATE TABLE Clubs (
    id INTEGER REFERENCES SportActivities(id) PRIMARY KEY,
    link VARCHAR
);

CREATE TABLE ClubLeaders (
    club_id INTEGER REFERENCES Clubs(id) PRIMARY KEY,
    user_id INTEGER REFERENCES Users(id) NOT NULL
);

CREATE TABLE Admins (
    id INTEGER REFERENCES Users(id) PRIMARY KEY
);

CREATE TABLE Students (
    id INTEGER REFERENCES Users(id) PRIMARY KEY
);

CREATE TABLE Hours (
    date DATE NOT NULL,
    student_id INTEGER REFERENCES Students(id) NOT NULL,
    activity_id INTEGER REFERENCES SportActivities(id) NOT NULL,
    hours_number INTEGER NOT NULL CHECK(hours_number > 0),
    PRIMARY KEY (date, student_id)
);

CREATE TABLE ClubParticipants(
    club_id INTEGER REFERENCES Clubs(id) NOT NULL,
    student_id INTEGER REFERENCES Students(id) NOT NULL,
    PRIMARY KEY (club_id, student_id)
);

CREATE TABLE PrimarySportActivities(
    student_id INTEGER REFERENCES Students(id) PRIMARY KEY,
    activity_id INTEGER REFERENCES SportActivities(id) NOT NULL
);