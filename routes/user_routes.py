from flask import Flask, Blueprint,request,jsonify,session,render_template
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


@user_bp.route("/signup", methods=["GET"])
def signupget():
    return render_template("signup.html")
@user_bp.route("/signup", methods=["POST"])
def signupgive():
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
            "message": "User added successfully"
        }),201


    except InvalidDataError as e:
        return jsonify({
            "error": str(e)
        }),400

    except UserAlreadyExistsError as e:
        return jsonify({
            "error": str(e)
        }),409


@user_bp.route("/login", methods=["GET"])
def loginget():
    return render_template("login.html")
@user_bp.route("/login", methods=["POST"])
def logingive():
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

        user = users.find_by_email(email)
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
@user_bp.route("/change-password-page")
@login_required
def change_password_page():

    return render_template("change_password.html")

@user_bp.route("/change-password", methods=["PUT"])
@login_required
def change_password():

    try:

        data = request.get_json()

        if not data:
            raise InvalidDataError(
                "Request data is required."
            )

        current_password = data.get("current_password")
        new_password = data.get("new_password")

        if not current_password or not new_password:
            raise InvalidDataError(
                "Current password and new password are required."
            )

        user = users.find_by_user_id(
            session["user_id"]
        )

        if user is None:
            raise UserNotFoundError(
                "User not found."
            )

        if not user.check_password(current_password):
            raise InvalidCredentialsError(
                "Current password is incorrect."
            )

        users.update_password(
            user.user_id,
            new_password
        )

        return jsonify({
            "message": "Password changed successfully."
        }), 200


    except InvalidDataError as e:

        return jsonify({
            "error": str(e)
        }), 400


    except InvalidCredentialsError as e:

        return jsonify({
            "error": str(e)
        }), 400


    except UserNotFoundError as e:

        return jsonify({
            "error": str(e)
        }), 404