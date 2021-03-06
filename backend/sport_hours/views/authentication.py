from flask_login import login_user, logout_user
from flask import request, abort
from sport_hours.blueprints import api
from sport_hours.models import User


@api.route('/login')
def login():
    if not 'email' in request.args:
        abort(400)
    user = User.query.get_or_404(request.args['email'])

    login_user(user, remember=True)
    return '', 204


@api.route('/logout')
def logout():
    logout_user()
    return '', 204
