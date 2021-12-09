from application import db, login_manager
from flask_login import UserMixin
import uuid

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20), nullable = False)
    lastname = db.Column(db.String(20), nullable = False)
    email = db.Column(db.String(30), unique = True, nullable = False)
    password = db.Column(db.String(60), nullable = False)

    def __repr__(self):
        return f"User('{self.email}', '{self.password}')"

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Integer, nullable = False)
    cardnum = db.Column(db.String, nullable = False, default = uuid.uuid4().hex[:8])
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"User('{self.user_id}', '{self.balance}')"