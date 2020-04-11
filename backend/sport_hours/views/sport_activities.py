from flask import request, abort
from flask.views import MethodView
from flask_login import login_required, current_user

from sport_hours.extensions import db
from sport_hours.blueprints import api
from sport_hours.models import User, SportActivity, Club
from sport_hours.schemas import SportActivitySchema, ClubSchema, UserSchema


@api.route('/activities')
@login_required
def get_assigned_activities():
    student = User.query.get_or_404(request.args.get('assigned_to'))
    out_schema = SportActivitySchema(many=True, exclude=('assigned_students',))
    return out_schema.jsonify(student.activities)


@api.route('/activities/all')
@login_required
def get_all_activities():
    activities = SportActivity.query.all()
    out_schema = SportActivitySchema(many=True, exclude=('assigned_students',))
    return out_schema.jsonify(activities)


@api.route('/activities/clubs/all')
@login_required
def get_all_clubs():
    clubs = Club.query.all()
    out_schema = ClubSchema(many=True)
    return out_schema.jsonify(clubs)


@api.route('/activities/<int:activity_id>', methods=['GET'])
@login_required
def get_activity_by_id(activity_id):
    activity = SportActivity.query.get_or_404(activity_id)

    out_schema = SportActivitySchema(many=False, exclude=('assigned_students',))
    return out_schema.jsonify(activity)


class AssignedStudentsAPI(MethodView):
    @login_required
    def get(self, activity_id):
        '''Get a list of students assigned to an activity.'''
        activity = SportActivity.query.get_or_404(activity_id)
        out_schema = UserSchema(many=True, exclude=('roles', 'activities'))
        return out_schema.jsonify(activity.assigned_students)

    @login_required
    def post(self, activity_id):
        if not current_user.is_admin():
            abort(401)
        
        '''Assign a given student to a sport activity.'''
        if not request.is_json:
            abort(400, 'The request must be in JSON.')

        if not isinstance(request.json.get('student_email'), str):
            abort(400, 'A valid student_email must be passed.')

        student = User.query.get_or_404(request.json['student_email'])
        activity = SportActivity.query.get_or_404(activity_id)

        activity.assigned_students.append(student)
        db.session.commit()
        return ('', 204)

    @login_required
    def delete(self, activity_id):
        if not current_user.is_admin():
            abort(401)
        
        '''Unassign a given student from a sport activity.'''
        if not request.is_json:
            abort(400, 'The request must be in JSON.')

        if not isinstance(request.json.get('student_email'), str):
            abort(400, 'A valid student_email must be passed.')

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
                 methods=('GET', 'POST', 'DELETE'))


@api.route('/activities/create', methods=['POST'])
@login_required
def create_sport_activity():
    if not current_user.is_admin():
        abort(401)
    
    in_schema = SportActivitySchema(exclude=('id',))
    activity_record = in_schema.load(request.json)

    db.session.add(activity_record)
    db.session.commit()

    return ('', 204)


@api.route('/activities/<int:activity_id>', methods=['PUT'])
@login_required
def modify_sport_activity(activity_id):
    if not current_user.is_admin():
        abort(401)
    
    in_schema = SportActivitySchema(exclude=('id',))
    record_in_db = SportActivity.query.get_or_404(activity_id)

    in_schema.load(request.json, session=db.session, instance=record_in_db, partial=True)

    db.session.commit()

    return ('', 204)


@api.route('/activities/<int:activity_id>', methods=['DELETE'])
@login_required
def delete_activity(activity_id):
    if not current_user.is_admin():
        abort(401)
    
    SportActivity.query.filter_by(id=activity_id).delete()
    db.session.commit()

    return ('', 204)


@api.route('/activities/clubs/<int:club_id>', methods=['PUT'])
@login_required
def create_club(club_id):
    if not current_user.is_admin():
        abort(401)
    
    SportActivity.query.get_or_404(club_id)

    in_schema = ClubSchema(exclude=('id',))
    record_in_db = Club.query.get(club_id)

    if record_in_db:
        in_schema.load(request.json, session=db.session, instance=record_in_db, partial=True)
    else:
        club_record = in_schema.load(request.json)
        club_record.id = club_id

        db.session.add(club_record)

    db.session.commit()

    return ('', 204)


@api.route('/activities/clubs/<int:club_id>', methods=['DELETE'])
@login_required
def delete_club(club_id):
    if not current_user.is_admin():
        abort(401)
    
    Club.query.filter_by(id=club_id).delete()
    db.session.commit()

    return ('', 204)
