from sport_hours.extensions import ma, db
from sport_hours.models import SportActivity, ActivityScheduleRecord


class SportActivitySchema(ma.ModelSchema):
    class Meta:
        model = SportActivity
        include_fk = True
        sqla_session = db.session

    schedule_records = ma.Nested('ActivityScheduleRecordSchema', many=True, exclude=('activity',))
    assigned_students = ma.Nested('UserSchema', many=True, exclude=('activities',))



class ActivityScheduleRecordSchema(ma.ModelSchema):
    class Meta:
        model = ActivityScheduleRecord
        include_fk = True  # will recognize the foreign key fields
        sqla_session = db.session
