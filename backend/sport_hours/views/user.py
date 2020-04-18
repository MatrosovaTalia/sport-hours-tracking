from flask import abort, request
from flask_login import login_required, current_user

from sport_hours.blueprints import api
from sport_hours.models import User
from sport_hours.schemas import UserSchema


@api.route('/users')
@login_required
def get_users():
    if not current_user.is_admin:
        abort(403)

    out_schema = UserSchema(many=True, exclude=('activities', 'roles'))
    return out_schema.jsonify(User.query.all())


@api.route('/user')
@login_required
def get_self():
    out_schema = UserSchema(exclude=('activities',))
    return out_schema.jsonify(current_user)
