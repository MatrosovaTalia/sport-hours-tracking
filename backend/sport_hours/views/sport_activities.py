from flask import request, abort
from flask.views import MethodView
from flask_login import login_required, current_user

from sport_hours.extensions import db
from sport_hours.blueprints import api
from sport_hours.models import User, SportActivity, ActivityScheduleRecord, activity_assignment
from sport_hours.schemas import SportActivitySchema


class ActivityAPI(MethodView):
    @login_required
    def get(self):
        '''Get a list of all activities.'''
        activities = SportActivity.query.all()
        out_schema = SportActivitySchema(many=True, exclude=('assigned_students',
                                                             'chat_link',
                                                             'schedule_records'))
        return out_schema.jsonify(activities)

    @login_required
    def post(self):
        '''Create a new activity.'''
        if not current_user.is_admin:
            abort(403)

        in_schema = SportActivitySchema(exclude=('id',))
        activity_record = in_schema.load(request.json)

        db.session.add(activity_record)
        db.session.commit()

        return ('', 204)

activity_api = ActivityAPI.as_view('activity_api')
api.add_url_rule('/activities', view_func=activity_api, methods=('GET', 'POST'))


@api.route('/activities/assigned')  # ?to=<email>
@login_required
def get_assigned_activities():
    if 'to' in request.args:
        if not current_user.is_admin and current_user.email != request.args['to']:
            abort(403)
        student = User.query.get_or_404(request.args['to'])
    else:
        student = current_user

    out_schema = SportActivitySchema(many=True, exclude=('assigned_students',
                                                         'chat_link',
                                                         'schedule_records'))
    return out_schema.jsonify(student.activities)


class ActivityDetailAPI(MethodView):
    @login_required
    def get(self, activity_id):
        '''Get detailed information about an activity.'''
        activity = SportActivity.query.get_or_404(activity_id)
        exclude = () if current_user.is_leader_of(activity_id) else ('assigned_students',)

        out_schema = SportActivitySchema(many=False, exclude=exclude)
        return out_schema.jsonify(activity)

    @login_required
    def patch(self, activity_id):
        '''Edit the activity.'''
        if not request.is_json:
            abort(400, 'The request must be in JSON.')

        if not current_user.is_admin and not current_user.is_leader_of(activity_id):
            abort(403)

        in_schema = SportActivitySchema(exclude=('id',))
        record_in_db = SportActivity.query.get_or_404(activity_id)

        for schedule_record in record_in_db.schedule_records:
            db.session.delete(schedule_record)

        in_schema.load(request.json, session=db.session, instance=record_in_db, partial=True)
        db.session.commit()

        return ('', 204)

    @login_required
    def delete(self, activity_id):
        '''Delete an activity.'''
        if not current_user.is_admin:
            abort(403)

        SportActivity.query.filter_by(id=activity_id).delete()
        db.session.commit()

        return ('', 204)

activity_detail_api = ActivityDetailAPI.as_view('activity_detail_api')
api.add_url_rule('/activities/<int:activity_id>',
                 view_func=activity_detail_api,
                 methods=('GET', 'PATCH', 'DELETE'))


class AssignedStudentsAPI(MethodView):
    @login_required
    def post(self, activity_id):
        '''Assign a given student to a sport activity.'''
        if not request.is_json:
            abort(400, 'The request must be in JSON.')

        if not isinstance(request.json.get('student_email'), str):
            abort(400, 'A valid student_email must be passed.')

        if not current_user.is_admin and current_user.email != request.json['student_email']:
            abort(403)

        student = User.query.get_or_404(request.json['student_email'])
        activity = SportActivity.query.get_or_404(activity_id)

        if (activity.max_students is not None
                and len(activity.assigned_students) >= activity.max_students):
            abort(400, 'Cannot assign any more students here.')

        activity.assigned_students.append(student)
        db.session.commit()

        return ('', 204)

    @login_required
    def delete(self, activity_id):
        '''Unassign a given student from a sport activity.'''
        if not request.is_json:
            abort(400, 'The request must be in JSON.')

        if not isinstance(request.json.get('student_email'), str):
            abort(400, 'A valid student_email must be passed.')

        if not current_user.is_admin  and current_user.email != request.json['student_email']:
            abort(403)

        student = User.query.get_or_404(request.json['student_email'])
        activity = SportActivity.query.get_or_404(activity_id)

        try:
            activity.assigned_students.remove(student)
        except ValueError:
            pass

        db.session.commit()
        return ('', 204)


asn_students_api = AssignedStudentsAPI.as_view('assigned_students_api')
api.add_url_rule('/activities/<int:activity_id>/assigned',
                 view_func=asn_students_api,
                 methods=('POST', 'DELETE'))


@api.route('/assign-randomly', methods=['POST'])
@login_required
def assign_randomly():
    '''Assign a given student to a random sport activity.'''
    if not request.is_json:
        abort(400, 'The request must be in JSON.')

    if not isinstance(request.json.get('student_email'), str):
        abort(400, 'A valid student_email must be passed.')

    if not current_user.is_admin:
        abort(403)

    student = User.query.get_or_404(request.json['student_email'])
    if len(student.activities) != 0:
        return '', 204

    student_count = db.func.count(activity_assignment.c.student_email)
    first_available = (
        # pylint: disable=bad-continuation
        SportActivity.query
            .outerjoin(activity_assignment)
            .group_by(SportActivity.id)
            .having(
                (SportActivity.max_students.is_(None))
                | (SportActivity.max_students > student_count)
            )
    ).first()
    first_available.assigned_students.append(student)
    db.session.commit()

    return ('', 204)
