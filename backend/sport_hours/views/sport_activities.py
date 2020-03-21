from flask import request, abort
from flask.views import MethodView

from sport_hours.extensions import db
from sport_hours.blueprints import api
from sport_hours.models import User, SportActivity, Club
from sport_hours.schemas import SportActivitySchema, ClubSchema


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


@api.route('/activities/clubs/all')
def get_all_clubs():
    clubs = Club.query.all()
    out_schema = ClubSchema(many=True)
    return out_schema.jsonify(clubs)


@api.route('/activity')
def get_activity_by_id():
    activity = SportActivity.query.filter_by(id=request.args.get('id')).one_or_none()

    if activity is None:
        return ('', 404)

    out_schema = SportActivitySchema(many=False, exclude=('assigned_students',))
    return out_schema.jsonify(activity)


@api.route('/activities/create', methods=['POST'])
def create_sport_activity():
    in_schema = SportActivitySchema(exclude=('id',))
    activity_record = in_schema.load(request.json)

    db.session.add(activity_record)
    db.session.commit()

    return ('', 204)


@api.route('/activities/<int:id>', methods=['PUT'])
def modify_sport_activity(id):
    in_schema = SportActivitySchema(exclude=('id',))
    record_in_db = SportActivity.query.filter_by(id=id).one_or_none()

    if record_in_db is None:
        return ('', 404)

    in_schema.load(request.json, session=db.session, instance=record_in_db, partial=True)
    
    db.session.commit()
    
    return ('', 204)


@api.route('/activities/<int:id>', methods=['DELETE'])
def delete_activity(id):
    SportActivity.query.filter_by(id=id).delete()
    db.session.commit()

    return ('', 204)


@api.route('/activities/clubs/<int:id>', methods=['PUT'])
def create_club(id):
    activity = SportActivity.query.filter_by(id=id).one_or_none()
    
    if activity is None:
        return ('', 404)

    in_schema = ClubSchema(exclude=('id',))
    record_in_db = Club.query.filter_by(id=id).one_or_none()

    if record_in_db:
        in_schema.load(request.json, session=db.session, instance=record_in_db, partial=True)
    else:
        club_record = in_schema.load(request.json)
        club_record.id = id

        db.session.add(club_record)
    
    db.session.commit()

    return ('', 204)


@api.route('/activities/clubs/<int:id>', methods=['DELETE'])
def delete_club(id):
    Club.query.filter_by(id=id).delete()
    db.session.commit()

    return ('', 204)
