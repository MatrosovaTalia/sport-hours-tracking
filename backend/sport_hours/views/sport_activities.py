from flask import request

from sport_hours.blueprints import api
from sport_hours.extensions import db
from sport_hours.models import SportActivity, SportHoursRecord, User
from sport_hours.schemas import SportHoursRecordSchema


@api.route('/activities/<int:activity_id>/attendance', methods=['POST'])
def track_attendance(activity_id):
    SportActivity.query.get_or_404(activity_id)

    in_schema = SportHoursRecordSchema(exclude=('id', 'activity_id'))
    hours_record = in_schema.load(request.json)
    hours_record.activity_id = activity_id

    User.query.get_or_404(hours_record.student_id)

    record_in_db = SportHoursRecord.query.filter_by(student_id=hours_record.student_id,
                                                    activity_id=hours_record.activity_id,
                                                    date=hours_record.date).one_or_none()
    if record_in_db:
        hours_record = in_schema.load(request.json, instance=record_in_db)
    db.session.add(hours_record)
    db.session.commit()
    return ('', 204)
