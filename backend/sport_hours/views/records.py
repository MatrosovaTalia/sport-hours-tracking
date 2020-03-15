from flask import request
from flask.views import MethodView

from sport_hours.blueprints import api
from sport_hours.extensions import db
from sport_hours.models import SportActivity, SportHoursRecord, User
from sport_hours.schemas import SportHoursRecordSchema



class SportHoursRecordAPI(MethodView):
    def get(self, activity_id):
        activity = SportActivity.query.get_or_404(activity_id)
        student = User.query.get_or_404(request.args.get('student_id'))

        records = (
            # pylint: disable=bad-continuation
            SportHoursRecord.query
                .filter_by(activity_id=activity.id, student_id=student.id)
                .order_by(SportHoursRecord.date.desc())
        )
        out_schema = SportHoursRecordSchema(many=True)

        return out_schema.jsonify(records.all())

    def post(self, activity_id):
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


record_api = SportHoursRecordAPI.as_view('sport_hours_record_api')
api.add_url_rule('/activities/<int:activity_id>/attendance',
                 view_func=record_api,
                 methods=('GET', 'POST'))