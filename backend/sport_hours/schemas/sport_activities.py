from sport_hours.extensions import ma, db
from sport_hours.models import SportActivity, Club, ActivityScheduleRecord
from sport_hours.schemas import UserSchema


class SportActivitySchema(ma.ModelSchema):
    class Meta:
        model = SportActivity
        sqla_session = db.session


class ClubSchema(ma.ModelSchema):
    class Meta:
        model = Club
        sqla_session = db.session
        include_fk = True


class ActivityScheduleRecordSchema(ma.ModelSchema):
    class Meta:
        model = ActivityScheduleRecord
        include_fk = True  # will recognize the foreign key fields
        sqla_session = db.session
