# Database schema

### User

Represents a general user of the application.
Attributes:
- **ID**: ```Serial, Primary Key``` 
- **Name**: ```String(128), Not Null```
- **Email**: ```String(64), Not Null```
- **Roles**: ```String(32)[]``` (student/admin/instructor/club leader)

## Sport activities

### Sport activity
- **ID**: ```Serial, Primary Key```
- **Name**: ```String(128), Not Null```

### Club
- **ID** ```Integer, Foreign Key ``` [(SportActivity.ID)](#sport-activity)```, Primary Key``` (the ID of the sport activity entity this club is associated with)
- **LeaderID** ```Integer, Foreign Key``` [(User.ID)](#user)```, Not Null``` (the ID of the user entity that is the leader of the club)
- **Link** ```String(256), Nullable``` (URL for the club description page)

## Records

### Sport hours record

- **ID**: ```Serial, Primary Key```
- **Date**: ```Date, Not Null``` (without time)
- **StudentID** ```Integer, Foreign Key``` [(User.ID)](#user) ```, Not Null``` 
- **ActivityID** ```Integer, Foreign Key``` [(SportActivity.ID)](#sport-activity)```, Not Null```
- **HoursNumber** ```Integer, Not Null``` (must be greater than 0)

### Activity assingment

A record that indicates that a student is assigned to some sport activity.

- **StudentID** ```Integer, Foreign Key``` [(User.ID)](#user)
- **ActivityID** ```Integer, Foreign Key``` [(SportActivity.ID)](#sport-activity)

```Primary Key``` is the tuple (**StudentID**, **ActivityID**) since it is a many-to-many relationship.

### Activity Schedule

- **ActivityID** ```Integer, Foreign Key``` [] [(SportActivity.ID)](#sport-activity)
- **Day** ```String(3)``` (day of the week in 3-letter format (e.g. "mon"))
- **StartTime** ```Time, Not Null```
- **FinishTime** ```Time, Not Null```
- **Location** ```String(64), Not Null``` (where the training is conducted)

```Primary Key``` is the tuple (**ActivityID**, **Day**).