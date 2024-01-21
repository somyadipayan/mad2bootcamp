from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, unset_jwt_cookies
from models import ma,db, bcrypt, User, user_schema, Theatre, theatre_schema, theatres_schema, Shows, show_schema, shows_schema, TransactionTable, transaction_schema, bookings_schema
from flask import Flask, request, Response, jsonify
from flask_cors import CORS
import datetime
from sqlalchemy import and_, or_, func
from tools.mailer import send_email
from flask_mail import Mail
from tools.workers import celery, ContextTask
from tools.task import add, test
from flask_caching import Cache


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'any_random_key'
app.config['MAIL_SERVER'] = 'localhost'
app.config['MAIL_PORT'] = 1025
app.config['CACHE_TYPE'] = 'redis'
app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/0'

mail = Mail(app)
cache = Cache(app)
jwt = JWTManager(app)

db.init_app(app)
ma.init_app(app)
bcrypt.init_app(app)
CORS(app, supports_credentials=True)
with app.app_context():
    db.create_all()

celery = celery

celery.conf.update(
    broker_url='redis://localhost:6379/1',
    result_backend='redis://localhost:6379/2'
)

celery.Task = ContextTask

app.app_context().push()

@app.route('/', methods = ['GET'])
def home():
    test.delay(to='managerorcreator@gmail.com')
    return "Hello World!"

@app.route('/register', methods = ['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    name = data.get('name')
    city = data.get('city')
    password = data.get('password')
    is_admin = data.get('is_admin')

    if not email or not name or not password:
        return jsonify({'error':'REQUIRED FIELDS CAN\'T BE EMPTY'}), 409

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'error':'Email is already Registered'}), 409

    new_user = User(email=email,
                    name=name,
                    city=city,
                    password=password,
                    is_admin=is_admin)
    
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message':'Registration Successful'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error':f'Some error occured {str(e)}'}), 409

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'error':'REQUIRED FIELDS CAN\'T BE EMPTY'}), 409

    user = User.query.filter_by(email=email).first()

    if not user or not bcrypt.check_password_hash(user.password, password):
        return jsonify({'error':'Invalid Credentials'}), 401
    
    access_token = create_access_token(identity={
        'id':user.id
    })

    return jsonify({"message":"Login Successful","access_token": access_token}), 200

@app.route('/logout',methods=['POST'])
@jwt_required()
def logout():
    response = jsonify({"message":"Logout Successful"})
    unset_jwt_cookies(response)
    return response, 200

@app.route('/fetchuserinfo', methods=['GET'])
@jwt_required()
def fetchuserinfo():
    this_user = get_jwt_identity()
    user = User.query.get(this_user['id'])
    if not user:
        return jsonify({'message': 'User not found'}), 404
    user_data = user_schema.dump(user)
    print(user_data)
    return jsonify(user_data), 200

@app.route('/protected',methods=['GET'])
@jwt_required()
def protected():
    return "You authorized to view this"

# CREATE THEATRE API
@app.route('/theatres', methods=['POST'])
@jwt_required()
def create_theatre():
    current_user = get_jwt_identity()
    user = User.query.get(current_user['id'])
    
    if not user.is_admin:
        return jsonify({'message': 'Access denied. You must be an admin to create a theatre.'}), 403

    data = request.json
    name = data.get('name')
    place = data.get('place')
    location = data.get('location')
    capacity = data.get('capacity')

    if not name or not place or not location or not capacity:
        return jsonify({'message': 'All fields are required'}), 400

    new_theatre = Theatre(name=name, place=place, location=location,
                          capacity=capacity, created_by=user.id)

    try:
        db.session.add(new_theatre)
        db.session.commit()
        return jsonify({'message': 'Theatre created successfully'}), 201
    except Exception as e:
        db.session.rollback()
        print(f"Error occurred while creating theatre: {str(e)}")
        return jsonify({'message': 'Error occurred while creating theatre'}), 500

# GET ALL THEATRES
@app.route('/theatres', methods=['GET'])
@jwt_required()
def get_all_theatres():
    current_user = get_jwt_identity()
    theatres = Theatre.query.filter_by(created_by=current_user['id']).all()
    result = theatres_schema.dump(theatres)
    return jsonify({'data':result})

# GET A SINGLE THEATRE by using it's ID
@app.route('/theatres/<int:theatre_id>', methods=['GET'])
@jwt_required()
def get_theatre(theatre_id):
    theatre = Theatre.query.get(theatre_id)
    if not theatre:
        return jsonify({'message': 'Theatre not found'}), 404

    result = theatre_schema.dump(theatre)
    return jsonify(result), 200

# UPDATE A THEATRE
@app.route('/theatres/<int:theatre_id>', methods=['PUT'])
@jwt_required()
def update_theatre(theatre_id):
    current_user = get_jwt_identity()
    user = User.query.get(current_user['id'])

    if not user or not user.is_admin:
        return jsonify({'message': 'Access denied. You must be an admin to edit a theatre.'}), 403

    theatre = Theatre.query.get(theatre_id)
    if not theatre:
        return jsonify({'message': 'Theatre not found'}), 404

    data = request.json
    name = data.get('name')
    place = data.get('place')
    location = data.get('location')
    capacity = data.get('capacity')

    if not name or not place or not location or not capacity:
        return jsonify({'message': 'All fields are required'}), 400

    theatre.name = name
    theatre.place = place
    theatre.location = location
    theatre.capacity = capacity

    try:
        db.session.commit()
        return jsonify({'message': 'Theatre updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error occurred while updating theatre: {str(e)}")
        return jsonify({'message': 'Error occurred while updating theatre'}), 500

# DELETE A THEATRE
@app.route('/theatres/<int:theatre_id>', methods=['DELETE'])
@jwt_required()
def delete_theatre(theatre_id):
    current_user = get_jwt_identity()
    user = User.query.get(current_user['id'])

    if not user or not user.is_admin:
        return jsonify({'message': 'Access denied. You must be an admin to delete a theatre.'}), 403

    theatre = Theatre.query.get(theatre_id)
    if not theatre:
        return jsonify({'message': 'Theatre not found'}), 404

    try:

        associated_shows = Shows.query.filter_by(theatre_id=theatre_id).all()
        for show in associated_shows:
            db.session.delete(show)

        db.session.delete(theatre)
        db.session.commit()

        return jsonify({'message': 'Theatre and associated shows are deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error occurred while deleting theatre: {str(e)}")
        return jsonify({'message': 'Error occurred while deleting theatre'}), 500


@app.route('/theatres/<int:theatre_id>/shows', methods=["GET"])
@cache.cached(timeout=600)
def get_all_shows(theatre_id):
    try:
        shows= Shows.query.filter_by(theatre_id=theatre_id).all()
        print(shows)
        return shows_schema.jsonify(shows)
    except Exception as e:
        return jsonify({'message': 'Error occurred while fetching shows', 'error': str(e)}), 500

@app.route('/clear_cache', methods=['POST'])
def clear_cache():
    cache.clear()
    return jsonify({'message':'SUCCESS'})

@app.route('/theatres/<int:theatre_id>/shows', methods=['POST'])
@jwt_required()  
def add_show_to_theatre(theatre_id):
    try:
        current_user = get_jwt_identity()
        user = User.query.get(current_user['id'])
        if not user or not user.is_admin:
            return jsonify({'message': 'Unauthorized. Only admin users can access this action.'}), 403

        data = request.get_json()
        name = data['name']
        tags = data['tags']
        rating = 0
        date_str = (data['date'])
        start_time_str = data['start_time']
        end_time_str = data['end_time']
        price = data['price']
        sold_ticket_count = 0

 
        date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
        start_time = datetime.datetime.strptime(start_time_str, '%H:%M').time()
        end_time = datetime.datetime.strptime(end_time_str, '%H:%M').time()

        # Check if the show timings overlap with existing shows in the same theatre
        existing_shows = Shows.query.filter(
            Shows.theatre_id == theatre_id,
            Shows.date == date,
            or_(
                and_(Shows.start_time <= start_time,
                     Shows.end_time > start_time),
                and_(Shows.start_time < end_time, Shows.end_time >= end_time),
            ),
        ).all()

        if existing_shows:
            return jsonify({'message': 'Show timings overlap with existing shows.'}), 400

        new_show = Shows(name, theatre_id, rating, tags, date,
                         start_time, end_time, price, sold_ticket_count)
        db.session.add(new_show)
        db.session.commit()

        return show_schema.jsonify(new_show)
    except Exception as e:
        return jsonify({'message': 'Error occurred while adding the show', 'error': str(e)}), 500
    

@app.route('/shows/<int:show_id>', methods=['GET'])
def get_show(show_id):
    try:
        show = Shows.query.filter_by(id=show_id).first()
        if not show:
            return jsonify({'message': 'Show not found'}), 404
        theatre = Theatre.query.get(show.theatre_id)
        remaining_tickets = theatre.capacity - show.sold_ticket_count
        data = {
            'show': show_schema.dump(show),
            'remaining_tickets': remaining_tickets,
        }

        return jsonify(data)

    except Exception as e:
        return jsonify({'message': 'Error occurred while fetching the show', 'error': str(e)}), 500
    
@app.route('/theatres/<int:theatre_id>/shows/<int:show_id>', methods=['PUT'])
@jwt_required() 
def edit_show(theatre_id, show_id):
    try:
        current_user = get_jwt_identity()
        user = User.query.get(current_user['id'])
        if not user or not user.is_admin:
            return jsonify({'message': 'Unauthorized. Only admin users can access this action.'}), 403


        show = Shows.query.filter_by(id=show_id, theatre_id=theatre_id).first()

        if not show:
            return jsonify({'message': 'Show not found'}), 404

        data = request.get_json()
        name = data['name']
        tags = data['tags']
        date_str = data['date']
        start_time_str = data['start_time']
        end_time_str = data['end_time']
        price = data['price']

        date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
        start_time = datetime.datetime.strptime(start_time_str, '%H:%M').time()
        end_time = datetime.datetime.strptime(end_time_str, '%H:%M').time()

        # Check if the show timings overlap with existing shows in the same theatre
        existing_shows = Shows.query.filter(
            Shows.theatre_id == theatre_id,
            Shows.date == date,
            Shows.id != show_id,
            or_(
                and_(Shows.start_time <= start_time,
                     Shows.end_time > start_time),
                and_(Shows.start_time < end_time,
                     Shows.end_time >= end_time),
            ),
        ).all()

        if existing_shows:
            return jsonify({'message': 'Show timings overlap with existing shows.'}), 400

        show.name = name
        show.tags = tags
        show.date = date
        show.start_time = start_time
        show.end_time = end_time
        show.price = price

        db.session.commit()

        return show_schema.jsonify(show)

    except Exception as e:
        return jsonify({'message': 'Error occurred while handling the show', 'error': str(e)}), 500



@app.route('/shows/<int:show_id>', methods=['DELETE'])
@jwt_required()  
def delete_show(show_id):
    try:
        current_user = get_jwt_identity()
        user = User.query.get(current_user['id'])
        if not user or not user.is_admin:
            return jsonify({'message': 'Unauthorized. Only admin users can access this action.'}), 403

        show = Shows.query.filter_by(id=show_id).first()

        if not show:
            return jsonify({'message': 'Show not found'}), 404
        
                
        transactions = TransactionTable.query.filter_by(show_id=show_id).all()
        for transaction in transactions:
            db.session.delete(transaction)
    
        db.session.delete(show)
        db.session.commit()

        return jsonify({'message': 'Show deleted successfully'}), 200

    except Exception as e:
        return jsonify({'message': 'Error occurred while deleting the show', 'error': str(e)}), 500


# book tickets for a show
@app.route('/book_ticket/<int:show_id>', methods=['POST'])
@jwt_required() 
def book_ticket(show_id):
    try:
        
        current_user = get_jwt_identity()
        user_id = current_user['id']

        show = Shows.query.get(show_id)
        show_name = show.name
        start_time = show.start_time.strftime('%H:%M')
        end_time = show.end_time.strftime('%H:%M')
        show_date = show.date.strftime('%Y-%m-%d')
        theatre_name = Theatre.query.get(show.theatre_id).name

        if not show:
            return jsonify({'message': 'Show not found'}), 404

        data = request.get_json()
        no_of_tickets = data['no_of_tickets']

        if no_of_tickets <= 0:
            return jsonify({'message': 'Invalid number of tickets'}), 400

        amount = no_of_tickets * show.price

        # Check if there are enough tickets available
        theatre = Theatre.query.get(show.theatre_id)
        remaining_tickets = theatre.capacity - show.sold_ticket_count
        if remaining_tickets < no_of_tickets:
            return jsonify({'message': 'Not enough tickets available'}), 400

        show.sold_ticket_count += no_of_tickets

        new_transaction = TransactionTable(user_id=user_id, show_id=show_id, date=datetime.datetime.today(), no_of_tickets=no_of_tickets, amount=amount)
        db.session.add(new_transaction)
        db.session.commit()

        # Send an email to the user with the ticket details

        return transaction_schema.jsonify(new_transaction)

    except Exception as e:
        return jsonify({'message': 'Error occurred while booking the ticket', 'error': str(e)}), 500

# API to fetch booking detail for a particular user
@app.route('/my_bookings', methods=['GET'])
@jwt_required()
def my_bookings():
    try:
        current_user = get_jwt_identity()
        user_id = current_user['id']

        bookings = TransactionTable.query \
                    .join(Shows, TransactionTable.show_id == Shows.id) \
                    .join(Theatre, Shows.theatre_id == Theatre.id) \
                    .add_columns(
                        TransactionTable.id,
                        TransactionTable.user_id,
                        TransactionTable.show_id,
                        TransactionTable.date,
                        TransactionTable.no_of_tickets,
                        TransactionTable.amount,
                        TransactionTable.rating,
                        Theatre.name.label('theatre_name'),
                        Shows.name.label('show_name')
                    ).filter(TransactionTable.user_id == user_id).all()

        booking_data = bookings_schema.dump(bookings)
        return jsonify(booking_data)

    except Exception as e:
        return jsonify({"message":"Some error Occured", "error":str(e)}), 500


# API endpoint to update the rating for a booking
@app.route('/update_rating', methods=['POST'])
@jwt_required()
def update_rating():
    try:
        data = request.json
        booking_id = data.get('booking_id')
        rating = data.get('rating')

        current_user = get_jwt_identity()
        user_id = current_user['id']

        booking = TransactionTable.query.filter_by(id=booking_id, user_id=user_id).first()

        if not booking:
            return jsonify({'message': 'Booking not found or does not belong to the current user'}), 404

        booking.rating = rating
        db.session.commit()

        show_id = booking.show_id
        average_rating = db.session.query(func.avg(TransactionTable.rating)).filter_by(show_id=show_id).scalar()

        show = Shows.query.filter_by(id=show_id).first()
        show.rating = average_rating
        db.session.commit()

        return jsonify({'message': 'Rating updated successfully'})

    except Exception as e:
        return jsonify({'message': 'Error occurred while updating rating', 'error': str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)