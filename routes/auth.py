import json

from flask import Blueprint,request,jsonify,session
# from app import config
import jwt
from werkzeug.security import generate_password_hash,check_password_hash
from exceptions.exceptions import handle_validation_error,unauthorized,not_found
from config.db import db
from model import User

auth = Blueprint('auth', __name__)

@auth.route('/register',methods=['POST'])
def register():
    data = request.get_json()
    email = data['email']
    password = data['password']
    """
    Things to do here
    - Validate email exists
    and return appropriate response
    """



    if not email or not password:
        jsonify({'message':'Email or password is required'}),400

    if len(password) < 8:
        jsonify({'message':'Password must be at least 8 characters long'}),400

    pass_hash = generate_password_hash(password)

    user =User(email=email,password=pass_hash)

    userEmail = db.session.query(User).filter(User.email==email).first()
    if userEmail:
        jsonify({'message':'User already exists'}),400


    db.session.add(user)
    db.session.commit()
    return jsonify({'message':'User registered successfully'})


@auth.post('/login')
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']
    if not(email or password):
        handle_validation_error({'message':'Username or password is required'})

    user = User.query.filter_by(email=email).first()

    if not user:
        not_found({'message':'User not found'})

    if not check_password_hash(user.password,password):
        unauthorized({'message':'Password is incorrect'})
    token = jwt.encode({
    "email":user.email
    },"ckdncndncljncjndscjbsd",algorithm="HS256")
    session['user_token'] = token
    session['user_id'] = user.id
    return jsonify({'message':'Login successful','user_token':token,'userInfo':{
        'id':user.id,
        'email':user.email,
    }})

@auth.route('/me')
def me():
    token = session.get('user_token')
    if not token:
        jsonify({'message':'User not found'}),404

    return jsonify({'message':'User successful'})

@auth.post('/logout')
def logout():
    session.pop('user_id', None)
    return jsonify({'message': 'Logout successful'}), 200