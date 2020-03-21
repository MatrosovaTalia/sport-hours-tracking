from flask import request

from sport_hours.blueprints import api
from sport_hours.models import User, SportActivity
from sport_hours.schemas import SportActivitySchema


@api.route('/activities')
def get_assigned_activities():
    student = User.query.get_or_404(request.args.get('assigned_to'))
    out_schema = SportActivitySchema(many=True, exclude=('assigned_students',))
    return out_schema.jsonify(student.activities)


@api.route('/activities/all')
def get_all_activities():
    activities = SportActivity.query.all()
    out_schema = SportActivitySchema(many=True, exclude=('assigned_students',))
    return out_schema.jsonify(activities)

@api.route('/activity')
def get_activity_by_id():
    activity = SportActivity.query.first_or_404(request.args.get('id'))
    out_schema = SportActivitySchema(many=False, exclude=('assigned_students',))
    return out_schema.jsonify(activity)