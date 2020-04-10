import re

from flask import Flask
from importlib import import_module
from flask_migrate import Migrate
from sport_hours.blueprints import all_blueprints

from sport_hours.extensions import db, cors, login_manager


def create_app():
    app = Flask(__name__) #name of current module
    app.config.from_pyfile('config/common.py')
    app.secret_key = app.config['SECRET_KEY']

    with app.app_context():
        import_module('sport_hours.models')


    db.init_app(app)  # conect extension (db) to our application (app)
    Migrate(app, db)

    cors.init_app(app, origins=[re.compile(r'https?://(?:localhost|0.0.0.0):\d{4}')], supports_credentials=True)
    login_manager.init_app(app)

    for blueprint in all_blueprints:
        import_module(blueprint.import_name)
        app.register_blueprint(blueprint)

    return app
