from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, unset_jwt_cookies
from models import ma,db, bcrypt, User, user_schema, Theatre, theatre_schema, theatres_schema
from flask import Flask, request, Response, jsonify
from flask_cors import CORS


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'any_random_key'

jwt = JWTManager(app)

db.init_app(app)
ma.init_app(app)
bcrypt.init_app(app)
CORS(app, supports_credentials=True)
with app.app_context():
    db.create_all()

app.app_context().push()

@app.route('/', methods = ['GET'])
def home():
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


if __name__ == "__main__":
    app.run(debug=True)