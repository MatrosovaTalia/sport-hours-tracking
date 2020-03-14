# Database schema

### User

Represents a general user of the application.
Attributes:
- **ID**: ```Serial, Primary Key``` 
- **First Name**: ```String(128), Not Null```
- **Last Name**: ```String(128), Not Null```

## Roles:

### Instructor
A trainer.
- **ID**: ```Integer, Primary Key, Foreign Key``` [(User.ID)](#User) (the ID of the user entity this instructor is associated with)

### Admin
A superuser.
- **ID**: ```Integer, Primary Key, Foreign Key``` [(User.ID)](#User) (the ID of the user entity this admin is associated with)

### Student
A student of the university.
- **ID**: ```Integer, Primary Key, Foreign Key``` [(User.ID)](#User) (the ID of the user entity this student is associated with)

## Sport activities

### Sport activity
- **ID**: ```Serial, Primary Key```
- **Name**: ```String(128), Not Null```

### Club
- **ID** ```Integer, Foreign Key ``` [(SportActivity.ID)](#sport-activity)```, Primary Key``` (the ID of the sport activity entity this club is associated with)
- **LeaderID** ```Integer, Foreign Key``` [(Student.ID)](#student)```, Not Null``` (the ID of the student entity that is the leader of the club)
- **Link** ```String(256), Nullable``` (URL for the club description page)

## Records

### Sport hours record

- **Date**: ```Date, Not Null``` (without time)
- **StudentID** ```Integer, Foreign Key``` [(Student.ID)](#student) ```, Not Null``` 
- **ActivityID** ```Integer, Foreign Key``` [(SportActivity.ID)](#sport-activity)```, Not Null```
- **HoursNumber** ```Integer, Not Null``` (must be greater than 0)

```Primary Key``` is the tuple (**Date**, **StudentId**) since a student is assumed to have only one record per day.

### Activity assingment

A record that indicates that a student is assigned to some sport activity.

- **StudentID** ```Integer, Foreign Key``` [(Student.ID)](#student)
- **ActivityID** ```Integer, Foreign Key``` [(SportActivity.ID)](#sport-activity)

```Primary Key``` is the tuple (**StudentID**, **ActivityID**) since it is a many-to-many relationship.
