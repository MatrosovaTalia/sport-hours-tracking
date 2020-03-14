from sport.extensions import ma
from sport_hours.models import SportActivity
from sport_hours.models import Club

class SportActivitySchema(ma.ModelSchema):
    class Meta:
        model = SportActivity

class ClubSchema(ma.ModelSchema):
    class Meta:
        model = Club