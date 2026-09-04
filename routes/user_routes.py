from flask import Flask, Blueprint,request,jsonify,session
from utils.db import mysql
from utils.decorators import login_required
from utils.exceptions import (
    InvalidDataError,
    InvalidAmountError,
    UserAlreadyExistsError,
    InvalidCredentialsError,
    UserNotFoundError   
)
from config import config
from models.user import users
user_bp=Blueprint("user",__name__)



@user_bp.route("/signup", methods=["POST"])
def signup():
    try:
        data = request.get_json()
        if not data:
            raise InvalidDataError(
                "Request data is required."
            )


        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

    
        if not username or not email or not password:
            raise InvalidDataError(
                "Username, email and password are required."
            )

    
        if users.find_by_email(email) is not None:
            raise UserAlreadyExistsError(
                "User already exists! Try logging in."
            )


        new_user = users.create(
            username,
            email,
            password
        )
        session["user_id"] = new_user.user_id
        return jsonify({
            "message": "User added successfully",
            "user": new_user.to_dict()
        }),201


    except InvalidDataError as e:
        return jsonify({
            "error": str(e)
        }),400

    except UserAlreadyExistsError as e:
        return jsonify({
            "error": str(e)
        }),409



@user_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        if not data:
            raise InvalidDataError(
                "Request data is required."
            )

        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            raise InvalidDataError(
                "Email and password are required."
            )

        user = user.find_by_email(email)
        if (
            user is None
            or not user.check_password(password)
        ):
            raise InvalidCredentialsError(
                "Invalid email or password."
            )

    
        session["user_id"] = user.user_id
        return jsonify({
            "message": "Login successful!",
            "user": user.to_dict()
        }), 200


    except InvalidDataError as e:
        return jsonify({
            "error": str(e)
        }),400
    except InvalidCredentialsError as e:
        return jsonify({
            "error": str(e)
        }),400


@user_bp.route("/logout", methods=["POST"])
@login_required
def logout():

    session.pop("user_id", None)
    return jsonify({
        "message": "Logout successful!"
    }),200


@user_bp.route("/profile", methods=["GET"])
@login_required
def profile():

    try:
        current_user = users.find_by_user_id(
            session["user_id"]
        )

        if current_user is None:
            raise UserNotFoundError(
                "User not found."
            )

        return jsonify({
            "message": "Your profile",
            "user": current_user.to_dict()
        }), 200

    except UserNotFoundError as e:
        return jsonify({
            "error": str(e)
        }), 404 
       