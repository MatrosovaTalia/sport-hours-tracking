from sport_hours.extensions import ma, db
from sport_hours.models import SportActivity, Club


class SportActivitySchema(ma.ModelSchema):
    class Meta:
        model = SportActivity
        sqla_session = db.session


class ClubSchema(ma.ModelSchema):
    class Meta:
        model = Club
        sqla_session = db.session
