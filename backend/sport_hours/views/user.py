from sport_hours.blueprints import api
from sport_hours.models import User
from sport_hours.schemas import UserSchema


@api.route('/users')
def get_users():
    out_schema = UserSchema(many=True, exclude=('activities', 'roles'))
    return out_schema.jsonify(User.query.all())