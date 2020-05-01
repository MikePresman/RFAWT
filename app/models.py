from app import app, db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    #role = db.Column(db.String(120))
    password_hash = db.Column(db.String(128))

    def check_password(self, password) -> bool:
        return check_password_hash(self.password_hash, password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        


class LocalNetwork(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pc_name = db.Column(db.String(64), index = True)
    ip_addr = db.Column(db.String(64), unique = True)
    port = db.Column(db.Integer)
    date_added = db.Column(db.String(120))



@login.user_loader
def load_user(id):
    return User.query.get(int(id))