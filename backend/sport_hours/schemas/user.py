from sport_hours.extensions import ma
from sport_hours.models import User

class UserSchema(ma.ModelSchema):
    class Meta:
        model = User