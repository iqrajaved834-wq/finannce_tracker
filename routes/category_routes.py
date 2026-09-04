from flask import Flask, Blueprint,request,jsonify,session
from utils.db import mysql
from utils.decorators import login_required
from utils.exceptions import (
    InvalidDataError,
    InvalidAmountError,
    InvalidCategoryError,
    CategoryNotFoundError
)
from config import config
from models.category import category
category_bp=Blueprint("category",__name__)


@category_bp.route("/categories", methods=["POST"])
@login_required
def create_category():

    try:
        data = request.get_json()
        if not data:
            raise InvalidDataError("Request data is required.")


        name = data.get("name")
        type = data.get("type")

        if not name:
            raise InvalidDataError("Category name is required.")
        if type not in ["income", "expense"]:
            raise InvalidDataError(
                "Type must be either income or expense."
            )

        
        category = category.create(
            session["user_id"],
            name,
            type
        )
        return jsonify({
            "message": "Category created successfully.",
            "category": category.to_dict()
        }), 201

    except InvalidDataError as e:
        return jsonify({
            "error": str(e)}),400





@category_bp.route('/categories',methods=["GET"])
@login_required
def get_category():
    try:
        categories=category.get_all(session["user_id"])
        if categories is None:
            raise CategoryNotFoundError("the user has no category!!!!!")
        return jsonify({"Categories":category.to_dict(category)for category in categories}),200

    except CategoryNotFoundError as e:
        return jsonify({"Error":str(e)}),404
