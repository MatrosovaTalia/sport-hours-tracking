from flask import request

from sport_hours.blueprints import api
from sport_hours.models import User
from sport_hours.schemas import SportActivitySchema


@api.route('/activities')
def get_assigned_activities():
    student = User.query.get_or_404(request.args.get('assigned_to'))
    out_schema = SportActivitySchema(many=True, exclude=('assigned_students',))
    return out_schema.jsonify(student.activities)
