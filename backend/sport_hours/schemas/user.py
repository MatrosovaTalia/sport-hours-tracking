from sport_hours.extensions import ma, db
from sport_hours.models import User


class UserSchema(ma.ModelSchema):
    class Meta:
        model = User
        sqla_session = db.session
