from sport_hours.extensions import ma, db
from sport_hours.models import SportActivity, ActivityScheduleRecord


class SportActivitySchema(ma.ModelSchema):
    class Meta:
        model = SportActivity
        sqla_session = db.session




class ActivityScheduleRecordSchema(ma.ModelSchema):
    class Meta:
        model = ActivityScheduleRecord
        include_fk = True  # will recognize the foreign key fields
        sqla_session = db.session
