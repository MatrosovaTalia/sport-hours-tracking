from sport.extensions import ma
from sport_hours.models import SportHoursRecords
from sport_hours.models import ActivityAssignments

class SportHoursSchema(ma.ModelSchema):
    class Meta:
        model = SportHoursRecords

class ActivityAssignmentSchema(ma.ModelSchema):
    class Meta:
        model = ActivityAssignments