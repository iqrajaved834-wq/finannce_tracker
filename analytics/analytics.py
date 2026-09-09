from flask import session
import pandas as pd
import matplotlib.pyplot as plt
from  utils.db import mysql

def get_data(id):

    cur = mysql.connection.cursor()
    query = """
        SELECT
            t.category_id,
            c.name AS categoryname,
            t.amount,
            t.transaction_date
        FROM transactions t
        JOIN categories c
            ON t.category_id = c.category_id
        WHERE t.type = 'expense' AND t.user_id=%s;
    """
    cur.execute(query,(id,))
    rows = cur.fetchall()
    cur.close()
    df = pd.DataFrame(rows)
    return df

def category_expense():
    id=session['user_id']
    df=get_data(id)
    if df.empty:
        return pd.Series(dtype='float64')
    df["amount"] = pd.to_numeric(df["amount"])
    df2=df.groupby("categoryname")['amount'].sum()
    return df2

def month_expense():
    id=session['user_id']
    df=get_data(id)
    if df.empty:
        return pd.Series(dtype='float64')
    df["amount"] = pd.to_numeric(df["amount"])
    df["transaction_date"]=pd.to_datetime(df["transaction_date"])
    df["month"]=df["transaction_date"].dt.strftime('%Y-%m')
    df3=df.groupby('month')['amount'].sum()
    return df3

def show_category():

    category = category_expense()

    plt.figure(figsize=(8, 5))

    if category.empty:

        plt.text(
            0.5,
            0.5,
            "No expense data available",
            ha="center",
            va="center"
        )

        plt.axis("off")

    else:

        category.plot(kind="bar")

        plt.xlabel("Categories")
        plt.ylabel("Expenses")
        plt.title("Expenses by Category")
        plt.xticks(rotation=45)

    plt.tight_layout()

    plt.savefig("static/category_expense.png")

    plt.close()

    
def show_month():

    month = month_expense()

    plt.figure(figsize=(8, 5))

    if month.empty:

        plt.text(
            0.5,
            0.5,
            "No expense data available",
            ha="center",
            va="center"
        )

        plt.axis("off")

    else:

        month.plot(kind="line", marker="o")

        plt.xlabel("Months")
        plt.ylabel("Expenses")
        plt.title("Expenses by Month")
        plt.xticks(rotation=45)

    plt.tight_layout()

    plt.savefig("static/month_expense.png")

    plt.close()

def total():
    id=session['user_id']
    df = get_data(id)
    if df.empty:
            return 0
    df['amount'] = pd.to_numeric(df['amount'])
    return df['amount'].sum()

def highest_category():
     id=session['user_id']
     df=get_data(id)
     if df.empty:
        return "No data"
     df["amount"] = pd.to_numeric(df["amount"])
     df2=df.groupby("categoryname")['amount'].sum()
     return df2.idxmax()

def highest_month():
    id=session['user_id']
    df=get_data(id)
    if df.empty:
        return "No data"
    df["amount"] = pd.to_numeric(df["amount"])
    df["transaction_date"]=pd.to_datetime(df["transaction_date"])
    df["month"]=df["transaction_date"].dt.strftime('%Y-%m')
    df3=df.groupby('month')['amount'].sum()
    return df3.idxmax()

def average_expense():
     id=session['user_id']
     df=get_data(id)
     if df.empty:
        return 0
     df["amount"] = pd.to_numeric(df["amount"])
     df["transaction_date"]=pd.to_datetime(df["transaction_date"])
     df["month"]=df["transaction_date"].dt.strftime('%Y-%m')
     df3=df.groupby('month')['amount'].sum()
     return df3.mean()