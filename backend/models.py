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

class Theatre(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    place = db.Column(db.Text, nullable=False)
    location = db.Column(db.Text, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    shows = db.relationship('Shows', back_populates='theatre')

    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    creator = db.relationship('User', backref='theatre')

    def __init__(self, name, place, location, capacity, created_by):
        self.name = name
        self.place = place
        self.location = location
        self.capacity = capacity
        self.created_by = created_by

class TheatreSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'place', 'location', 'capacity', 'created_by')

theatre_schema = TheatreSchema()
theatres_schema = TheatreSchema(many=True)


class Shows(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    theatre_id = db.Column(db.Integer, db.ForeignKey('theatre.id'), nullable=False)
    rating = db.Column(db.Float)
    tags = db.Column(db.Text)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    price = db.Column(db.Float, nullable=False)
    sold_ticket_count = db.Column(db.Integer, nullable=False)
    theatre = db.relationship('Theatre', back_populates='shows')
    
    def __init__(self, name, theatre_id, rating, tags, date, start_time, end_time, price, sold_ticket_count):
        self.theatre_id = theatre_id
        self.name = name
        self.rating = rating
        self.tags = tags
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.price = price
        self.sold_ticket_count = sold_ticket_count

class ShowsSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'theatre_id', 'rating', 'tags', 'date', 'start_time', 'end_time', 'price', 'sold_ticket_count')

show_schema = ShowsSchema()
shows_schema = ShowsSchema(many=True)