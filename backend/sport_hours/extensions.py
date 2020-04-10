
"""Flask extensions are instantiated here.
To avoid circular imports with views and create_app(), extensions are instantiated here.
They will be initialized (calling init_app()) in app.py.
"""


from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS


cors = CORS()

ma = Marshmallow()
db = SQLAlchemy()
login_manager = LoginManager()
