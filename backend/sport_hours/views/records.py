from flask import request, abort
from flask.views import MethodView
from flask_login import login_required, current_user

from sport_hours.blueprints import api
from sport_hours.extensions import db
from sport_hours.models import SportActivity, SportHoursRecord, User
from sport_hours.schemas import SportHoursRecordSchema


class SportHoursRecordAPI(MethodView):
    @login_required
    def get(self, activity_id):
        if not (current_user.is_admin or
                current_user.email == request.args['student_email'] or
                current_user.is_leader_of(activity_id)):
            abort(403)
        activity = SportActivity.query.get_or_404(activity_id)
        student = User.query.get_or_404(
            request.args.get('student_email', current_user.email)
        )

        records = (
            # pylint: disable=bad-continuation
            SportHoursRecord.query
                .filter_by(activity_id=activity.id, student_email=student.email)
                .order_by(SportHoursRecord.date.desc())
        )
        out_schema = SportHoursRecordSchema(many=True)

        return out_schema.jsonify(records.all())

    @login_required
    def post(self, activity_id):
        if not (current_user.is_admin or
                current_user.is_leader_of(activity_id)):
            abort(403)

        SportActivity.query.get_or_404(activity_id)

        in_schema = SportHoursRecordSchema(exclude=('id', 'activity_id'))
        hours_record = in_schema.load(request.json)
        hours_record.activity_id = activity_id

        User.query.get_or_404(hours_record.student_email)

        record_in_db = SportHoursRecord.query.filter_by(student_email=hours_record.student_email,
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
