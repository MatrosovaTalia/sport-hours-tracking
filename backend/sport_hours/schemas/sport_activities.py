from sport.extensions import ma
from sport_hours.models import SportActivities
from sport_hours.models import Clubs

class SportActivitySchema(ma.ModelSchema):
    class Meta:
        model = SportActivities

class ClubSchema(ma.ModelSchema):
    class Meta:
        model = Clubs