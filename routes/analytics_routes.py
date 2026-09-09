from flask import Flask, Blueprint,request,jsonify,session,render_template
from utils.db import mysql
from utils.decorators import login_required
from utils.exceptions import (
    InvalidDataError,
    InvalidAmountError,
    InvalidCategoryError,
    CategoryNotFoundError
)
import pandas as pd
from config import config
from analytics.analytics import (
    show_month,
    show_category,
    total,
    highest_category,
    highest_month,
    average_expense
)
analytics_bp=Blueprint("analytics",__name__)
@analytics_bp.route("/analytics")
@login_required
def analytics():

    show_month()
    show_category()

    total_expense = total()
    category = highest_category()
    month = highest_month()
    average = average_expense()

    return render_template(
        "analytics.html",
        total_expense=total_expense,
        highest_category=category,
        highest_month=month,
        average_expense=average
    )