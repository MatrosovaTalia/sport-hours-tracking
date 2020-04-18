from flask_login.mixins import UserMixin

from sport_hours.models.sport_activities import Club
from sport_hours.extensions import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    email = db.Column(db.String(128), primary_key=True)
    full_name = db.Column(db.String(128), nullable=False)
    roles = db.Column(postgresql.ARRAY(db.String(32)), nullable=False)
    # property `activities` available with a backref

    def get_id(self):
        """Return the user's e-mail."""
        return self.email
    
    @property
    def is_admin(self):
        return 'admin' in self.roles

    @property
    def is_trainer(self):
        return 'trainer' in self.roles
    
    def is_leader_of(self, activity_id):
        return db.exists(Club.query.filter_by(id=activity_id, leader=self.email))

