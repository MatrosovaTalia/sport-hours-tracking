from flask import abort
from flask_login import login_required, current_user

from sport_hours.blueprints import api
from sport_hours.extensions import db
from sport_hours.models import User, activity_assignment
from sport_hours.schemas import UserSchema


@api.route('/users')
def get_users():
    out_schema = UserSchema(many=True, exclude=('activities',))
    return out_schema.jsonify(User.query.all())


@api.route('/user')
@login_required
def get_self():
    out_schema = UserSchema(exclude=('activities',))
    return out_schema.jsonify(current_user)


@api.route('/users/unassigned')
@login_required
def get_unassigned():
    if not current_user.is_admin:
        abort(403)

    activity_count = db.func.count(activity_assignment.c.activity_id)
    users = User.query.outerjoin(activity_assignment).group_by(User).having(activity_count == 0)
    out_schema = UserSchema(exclude=('activities',), many=True)
    return out_schema.jsonify(users.all())
