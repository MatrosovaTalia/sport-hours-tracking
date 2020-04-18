from flask import abort, request
from flask_login import login_required, current_user

from sport_hours.blueprints import api
from sport_hours.models import User
from sport_hours.schemas import UserSchema


@api.route('/users')
def get_users():

    out_schema = UserSchema(many=True, exclude=('activities', 'roles'))
    return out_schema.jsonify(User.query.all())


@api.route('/user')
@login_required
def get_self():
    out_schema = UserSchema(exclude=('activities',))
    return out_schema.jsonify(current_user)
