from application import db, login_manager
from flask_login import UserMixin #We are importing UserMixin since Flask requires a user model for properties such as is_authenticated, is_active, etc.
import uuid #We are importing uuid class to generate a unique id/number for our leap card which gets automatically assigned to the user.

@login_manager.user_loader #This code is used for flask_login to understand what details are considered for the current user based on id.
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
    cardnum = db.Column(db.String, nullable = False, default = uuid.uuid4().hex[:8]) #we generate a card number for the user here
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"User('{self.user_id}', '{self.balance}')"