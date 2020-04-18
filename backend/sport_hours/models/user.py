from flask_login.mixins import UserMixin

from sport_hours.extensions import db, login_manager
from sport_hours.models.sport_activities import SportActivity


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    email = db.Column(db.String(128), primary_key=True)
    full_name = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    # property `activities` available with a backref

    def get_id(self):
        """Return the user's e-mail."""
        return self.email

    def is_leader_of(self, activity_id):
        activity = SportActivity.query.filter_by(id=activity_id, leader=self.email)
        return db.session.query(activity.exists()).scalar()
