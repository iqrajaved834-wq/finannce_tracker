from flask import Flask, Blueprint, request, jsonify, session, render_template
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
    get_data,
    show_month,
    show_category,
    total,
    highest_category,
    highest_month,
    average_expense
)

analytics_bp = Blueprint("analytics", __name__)
@analytics_bp.route("/analytics")
@login_required
def analytics():

    id = session["user_id"]
    period = request.args.get("period","all_time")
    df = get_data(id, period)

    show_month(df)
    show_category(df)

    total_expense = total(df)
    category = highest_category(df)
    month = highest_month(df)
    average = average_expense(df)

    return render_template(
        "analytics.html",
        total_expense=total_expense,
        highest_category=category,
        highest_month=month,
        average_expense=average
    )