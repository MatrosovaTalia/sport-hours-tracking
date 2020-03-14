from sport.extensions import ma
from sport_hours.models import SportHours
from sport_hours.models import ActivityAssignment

class SportHoursSchema(ma.ModelSchema):
    class Meta:
        model = SportActivity

class ActivityAssignmentSchema(ma.ModelSchema):
    class Meta:
        model = ActivityAssignment