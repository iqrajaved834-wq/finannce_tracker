from flask import Flask, request, jsonify, session
from config import config
from utils.db import mysql
from models.user import users
from utils.decorators import login_required

app = Flask(__name__)
app.config.from_object(config)
mysql.init_app(app)

@app.route('/')
def home():
    return "Finance tracker is live!!!"

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({"error": "username, email, password all three are required!"}), 400
    if users.find_by_email(email) is not None:
        return jsonify({"error": "User already exists! Try logging in."}), 409

    user = users.create(username, email, password)
    session['user_id'] = user.user_id
    return jsonify({"message": "User added successfully", "user": user.to_dict()}), 201

@app.route("/login", methods=['POST'])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required!"}), 400

    user = users.find_by_email(email)
    if user is None or not user.check_password(password):
        return jsonify({"error": "Invalid email or password"}), 401

    session['user_id'] = user.user_id
    return jsonify({"message": "Login successful!", "user": user.to_dict()}), 200

@app.route("/logout", methods=['POST'])
@login_required
def logout():
    session.pop('user_id', None)
    return jsonify({"message": "Logout successful!"}), 200

@app.route('/profile', methods=['GET'])
@login_required
def profile():
    user = users.find_by_user_id(session['user_id'])
    return jsonify({"message": "Your profile", "user": user.to_dict()}), 200

if __name__ == '__main__':
    app.run(debug=True)