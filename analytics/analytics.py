from flask import session
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from  utils.db import mysql

def get_data(id, period):

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
        WHERE t.type = 'expense'
        AND t.user_id = %s
    """

    if period == "this_month":

        query += """
            AND YEAR(t.transaction_date) = YEAR(CURDATE())
            AND MONTH(t.transaction_date) = MONTH(CURDATE())
        """

    elif period == "last_month":

        query += """
            AND YEAR(t.transaction_date) =
                YEAR(DATE_SUB(CURDATE(), INTERVAL 1 MONTH))
            AND MONTH(t.transaction_date) =
                MONTH(DATE_SUB(CURDATE(), INTERVAL 1 MONTH))
        """

    elif period == "this_year":

        query += """
            AND YEAR(t.transaction_date) = YEAR(CURDATE())
        """

    elif period == "all_time":

        pass

    query += " ORDER BY t.transaction_date"

    cur.execute(query, (id,))

    rows = cur.fetchall()

    cur.close()

    df = pd.DataFrame(rows)

    return df

# def category_expense():
#     id=session['user_id']
#     df=get_data(id)
#     if df.empty:
#         return pd.Series(dtype='float64')
#     df["amount"] = pd.to_numeric(df["amount"])
#     df2=df.groupby("categoryname")['amount'].sum()
#     return df2

# def month_expense():
#     id=session['user_id']
#     df=get_data(id)
#     if df.empty:
#         return pd.Series(dtype='float64')
#     df["amount"] = pd.to_numeric(df["amount"])
#     df["transaction_date"]=pd.to_datetime(df["transaction_date"])
#     df["month"]=df["transaction_date"].dt.strftime('%Y-%m')
#     df3=df.groupby('month')['amount'].sum()
#     return df3

def show_category(df):
    if (df.empty):
     category= pd.Series(dtype='float64')
    else:
     df["amount"] = pd.to_numeric(df["amount"])
     category=df.groupby("categoryname")['amount'].sum()
  

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

    
def show_month(df):
    if (df.empty):
      month= pd.Series(dtype='float64')
    else:
      df["amount"] = pd.to_numeric(df["amount"])
      df["transaction_date"]=pd.to_datetime(df["transaction_date"])
      df["month"]=df["transaction_date"].dt.strftime('%Y-%m')
      month=df.groupby('month')['amount'].sum()
    

    plt.figure(figsize=(8, 5))
    if (month.empty):

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

def total(df):

    if df.empty:
            return 0
    else:
     df['amount'] = pd.to_numeric(df['amount'])
     return df['amount'].sum()

def highest_category(df):
    
    if df.empty:
        return "No data"
    else:
       df["amount"] = pd.to_numeric(df["amount"])
       df2=df.groupby("categoryname")['amount'].sum()
       return df2.idxmax()

def highest_month(df):
    
    if df.empty:
        return "No data"
    else:
     df["amount"] = pd.to_numeric(df["amount"])
     df["transaction_date"]=pd.to_datetime(df["transaction_date"])
     df["month"]=df["transaction_date"].dt.strftime('%Y-%m')
     df3=df.groupby('month')['amount'].sum()
     return df3.idxmax()

def average_expense(df):
     if df.empty:
        return 0
     else:
      df["amount"] = pd.to_numeric(df["amount"])
      df["transaction_date"]=pd.to_datetime(df["transaction_date"])
      df["month"]=df["transaction_date"].dt.strftime('%Y-%m')
      df3=df.groupby('month')['amount'].sum()
      return df3.mean()