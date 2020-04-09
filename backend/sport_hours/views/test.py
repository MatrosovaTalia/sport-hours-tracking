from flask_login import login_user, logout_user
from flask import current_app, url_for, redirect, session, request
from sport_hours.blueprints import api
from flask_login import login_required, current_user

@login_required
@api.route('/test')
def test():
    print(request.args)
    return ''
