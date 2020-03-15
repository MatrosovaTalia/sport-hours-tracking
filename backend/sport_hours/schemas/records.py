from marshmallow import validate

from sport_hours.extensions import ma, db
from sport_hours.models import SportHoursRecord


class SportHoursRecordSchema(ma.ModelSchema):
    class Meta:
        model = SportHoursRecord
        include_fk = True  # will recognize the foreign key fields
        sqla_session = db.session

    hours_number = ma.Int(validate=validate.Range(min=1))
