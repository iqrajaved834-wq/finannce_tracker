from utils.db import mysql
class transaction:
    table_name="transactions"

def __init__(self,transaction_id,user_id,category_id,amount,type,description,transaction_date):
        self.transaction_id = transaction_id
        self.user_id = user_id
        self.category_id = category_id
        self.amount = amount
        self.type = type
        self.description = description
        self.transaction_date = transaction_date

def to_dict(self):
        return {
            "transaction_id": self.transaction_id,
            "user_id": self.user_id,
            "category_id": self.category_id,
            "amount": float(self.amount),
            "type": self.type,
            "description": self.description,
            "transaction_date": str(self.transaction_date)
        }

@staticmethod
def from_row(row):
       return transaction(
            row["transaction_id"],
            row["user_id"],
            row["category_id"],
            row["amount"],
            row["type"],
            row["description"],
            row["transaction_date"]
       )

#we can use find_by_id function because we have that in base class and we have set our table_name

@staticmethod
def create(
    user_id,
    category_id,
    amount,
    type,
    description,
    transaction_date
):
    cur = mysql.connection.cursor()
    cur.execute(
        """
        INSERT INTO transactions
        (user_id, category_id, amount, type, description, transaction_date)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (
            user_id,
            category_id,
            amount,
            type,
            description,
            transaction_date
        )
    )

    mysql.connection.commit()
    new_id = cur.lastrowid
    cur.close()

    return transaction(
        new_id,
        user_id,
        category_id,
        amount,
        type,
        description,
        transaction_date
    )

@staticmethod
def find_by_user(self,user_id):
      cur=mysql.connection.cursor()
      cur.execute(
            """"select * from transactions where user_id=%s
                order by transaction_date  DESC""",(user_id,))
      rows=cur.fetchall()
      cur.close()
      return {transaction.from_row(row)for row in rows}

@staticmethod
def find_by_user(category_id):
    cur = mysql.connection.cursor()

    cur.execute(
        """
        SELECT *
        FROM categories
        WHERE category_id = %s
        """,
        (category_id,)
    )

    row = cur.fetchone()
    cur.close()
    if row is not None:
     return{transaction.from_row(row)for row in row}
@staticmethod
def find_by_user(self,user_id,month,category_id):
      cur=mysql.connection.cursor()
      query="select * from transaction where user_id=%s"
      param=[user_id]

      if month:
            query+="And Data_format(transaction_date,'%%y-%%m)'=%s"
            param.append[month]
      if category_id:
            query+="And category_id=%s"
            param[category_id]

      "order by transaction_date DESC"

      cur.execute(query,tuple(param))
      rows=cur.fetchall()
      cur.close()
      return {transaction.from_row(row)for row in rows}

@staticmethod
def update_transaction(
          transaction_id,
          user_id,
          category_id,
          amount,
          type,
          description,
          transaction_date
):
      cur=mysql.connection.cursor()
      query="""update transactions
             "set
             category_id=%s 
             amount = %s,
             type = %s,
             description = %s,
             transaction_date = %s
             where transaction_id=%s And user_id=%s"""
      cur.execute(query,(
             category_id,
            amount,
            type,
            description,
            transaction_date,
            transaction_id,
            user_id
      ))
      mysql.connection.commit()
      affected_rows=cur.rowcount
      cur.close()
      return (affected_rows)

@staticmethod
def delete(transaction_id, user_id):

    cur = mysql.connection.cursor()
    cur.execute(
        """
        DELETE FROM transactions
        WHERE transaction_id = %s
        AND user_id = %s
        """,
        (transaction_id, user_id)
    )

    mysql.connection.commit()
    affected_rows = cur.rowcount
    cur.close()
    return affected_rows
      
    
      
      