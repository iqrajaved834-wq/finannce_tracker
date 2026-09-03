from  utils.db import mysql


class category:

    table_name = "categories"

    def __init__(self, category_id, user_id, name, type):
        self.category_id = category_id
        self.user_id = user_id
        self.name = name
        self.type = type

    def to_dict(self):
            return {
                "category_id": self.category_id,
                "user_id": self.user_id,
                "name": self.name,
                "type": self.type
            }

    
    @staticmethod
    def from_row(row):
        return category(
            row["category_id"],
            row["user_id"],
            row["name"],
            row["type"]
        )

    @staticmethod
    def create(user_id, name, category_type):
        cur = mysql.connection.cursor()

        cur.execute(
        """
        INSERT INTO categories (user_id, name, type)
        VALUES (%s, %s, %s)
        """,
        (user_id, name, category_type))

        mysql.connection.commit()
        new_id = cur.lastrowid
        cur.close()

        return category(
        new_id,
        user_id,
        name,
        category_type
    )

    @staticmethod
    def get_all(user_id):
         cur=mysql.connection.cursor()
         cur.execute("""select * from categories where user_id is null or user_id=%s""",(user_id,))
         rows=cur.fetchall()
         cur.close()
         return {category.from_row(row)for row in rows}



    