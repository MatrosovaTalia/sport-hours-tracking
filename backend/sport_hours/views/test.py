from sport_hours.blueprints import api

@api.route('/holyshit')
def view():
    return 'holy shit'