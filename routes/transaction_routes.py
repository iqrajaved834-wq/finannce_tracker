from flask import Blueprint, request, jsonify, session
import datetime
from config import config
from utils.db import mysql
from utils.decorators  import login_required
from utils.exceptions import(
    InvalidDataError,
    InvalidAmountError,
    InvalidCategoryError,
    CategoryNotFoundError,
    InvalidTransactionTypeError,
    TransactionNotFoundError)
from models.transaction import transaction
transaction_bp=Blueprint("transaction",__name__)


@transaction_bp.route("/transactions",methods=["POST"])
@login_required
def transaction_create():
    try:
        data=request.get_json()
        if data is None:
          raise InvalidDataError("It is must to enter the data!!!")

        
        amount = data.get("amount")
        category_id = data.get("category_id")
        type = data.get("type")
        description = data.get("description")
        transaction_date = data.get("transaction_date")


        if amount is None:
           raise InvalidAmountError("It is must to enter some amount!!!")
        try:
               amount=float(amount)    
        except (TypeError,ValueError):
               raise InvalidAmountError("It is must to eneter amount in numbers!!!")
        if amount<=0:
            raise InvalidAmountError("The amount must be positive number greater tahn zero!!!!!")

        
       
        if category_id is None:
            raise InvalidCategoryError("It is must to enter category ID!!!")
        try:
            category_id=int(category_id)
        except(TypeError,ValueError):
            raise InvalidCategoryError("It is must to enter Integer(0,1,2,3) category ID!!!")
        if transaction.find_by_category(category_id) is None:
            raise CategoryNotFoundError("This category_id not exist!!!")
        

        if type not in["income","expense"]:
                raise InvalidTransactionTypeError("Transaction type must be income or expense!!!!")
        if description is None or transaction_date is None:
                raise InvalidDataError("It is must tto enter alll the credentials!!!!")
        

        tran=tran = transaction.create(
    session["user_id"],
    category_id,
    amount,
    type,
    description,
    transaction_date
)
        return jsonify({"message":"Transaction created successfully!!!","Transaction":transaction.to_dict(tran)}),201

    
    except InvalidDataError as e:
        return jsonify({"Error":str(e)}),400
    except InvalidAmountError as e:
        return jsonify({"error": str(e)}), 400

    except InvalidCategoryError as e:
        return jsonify({"error": str(e)}), 400

    except CategoryNotFoundError as e:
        return jsonify({"error": str(e)}), 404

    except InvalidTransactionTypeError as e:
        return jsonify({"error": str(e)}), 400

    

@transaction_bp.route("/transactions", methods=["GET"])
@login_required
def transaction_get():

    user_id = session["user_id"]

    month = request.args.get("month")
    category_id = request.args.get("category_id")

    if month:
        try:
            datetime.datetime.strptime(month, '%Y-%m')
        except ValueError:
            return jsonify({
                "Error": "The month must be in YYYY-MM format!"
            }), 400

    if category_id:
        try:
            category_id = int(category_id)

            if category_id <= 0:
                raise InvalidCategoryError(
                    "There must be category greater than 0"
                )

        except (TypeError, ValueError):
            return jsonify({
                "Error": "The category_id must be an integer!"
            }), 400

        except InvalidCategoryError as e:
            return jsonify({
                "Error": str(e)
            }), 400

    transactions = transaction.find_by_umc(
        user_id,
        month,
        category_id
    )

    return jsonify({
        "Transaction": [
            t.to_dict()
            for t in transactions
        ]
    }), 200


@transaction_bp.route("/transactions/<int:transaction_id>", methods=["PUT"])
@login_required
def update_transaction(transaction_id):
    try:
        data=request.get_json()
        if data is None:
          raise InvalidDataError("It is must to enter the data!!!")

        
        amount = data.get("amount")
        category_id = data.get("category_id")
        type = data.get("type")
        description = data.get("description")
        transaction_date = data.get("transaction_date")



        if amount is None:
           raise InvalidAmountError("It is must to enter some amount!!!")
        try:
               amount=float(amount)    
        except (TypeError,ValueError):
               raise InvalidAmountError("It is must to eneter amount in numbers!!!")
        if amount<=0:
            raise InvalidAmountError("The amount must be positive number greater tahn zero!!!!!")
    
        

        if category_id is None:
            raise InvalidCategoryError("It is must to enter category ID!!!")
        try:
            category_id=int(category_id)
        except(TypeError,ValueError):
            raise InvalidCategoryError("It is must to enter Integer(0,1,2,3) category ID!!!")
        if transaction.find_by_category(category_id) is None:
            raise CategoryNotFoundError("This category_id not exist!!!") 
        

        if type not in["income","expense"]:
                raise InvalidTransactionTypeError("Transaction type must be income or expense!!!!")
        if description is None or transaction_date is None:
                raise InvalidDataError("It is must tto enter alll the credentials!!!!")

        affectedrow=transaction.update(
             transaction_id,
             session["user_id"],
             category_id,
             amount,type,description,transaction_date
        )
        if affectedrow==0:
             raise TransactionNotFoundError("Transaction on this ID not fopund!!!!!")
        return jsonify({"Message":"Transaction oon this Id is updates successfully!!!"}),201
    

    except InvalidDataError as e:
         return jsonify({"Mesaage":str(e)}),400
    except InvalidAmountError as e:
        return jsonify({"error": str(e)}), 400

    except InvalidCategoryError as e:
        return jsonify({"error": str(e)}), 400

    except InvalidTransactionTypeError as e:
        return jsonify({"error": str(e)}), 400

    except TransactionNotFoundError as e:
        return jsonify({"error": str(e)}), 404

    
    

@transaction_bp.route( "/transactions/<int:transaction_id>",methods=["DELETE"])
@login_required
def delete_transaction(transaction_id):

    try:
        affected_rows = transaction.delete(
            transaction_id,
            session["user_id"]
        )

        if affected_rows == 0:
            raise TransactionNotFoundError(
                "Transaction not found."
            )

        return jsonify({
            "message": "Transaction deleted successfully."
        }), 200

    except TransactionNotFoundError as e:
        return jsonify({
            "error": str(e)
        }), 404