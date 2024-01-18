from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from marshmallow import fields

db = SQLAlchemy()
ma = Marshmallow()
bcrypt = Bcrypt()

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    email = db.Column(db.Text, unique = True, nullable = False)
    name = db.Column(db.Text, nullable = False)
    city = db.Column(db.Text)
    password = db.Column(db.Text, nullable = False)
    is_admin = db.Column(db.Boolean, nullable= False, default = False)

    def __init__(self, email, name, city, password, is_admin):
        self.email = email
        self.name = name
        self.city = city
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
        self.is_admin = is_admin

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'email', 'name', 'city', 'is_admin')

user_schema = UserSchema()
users_schema = UserSchema(many = True)