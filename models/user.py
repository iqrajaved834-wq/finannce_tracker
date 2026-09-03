import bcrypt
from utils.db import mysql

class users:
    def __init__(self, user_id, username, email, hash_password):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.hash_password = hash_password

    def to_dict(self):
            return {"user_id": self.user_id, "username": self.username, "email": self.email}
    
    def check_password(self, plain_password: str) -> bool:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"),
            self.hash_password.encode("utf-8")
        )

    @staticmethod
    def generate_hash(plain_password: str) -> str:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(plain_password.encode("utf-8"), salt)
        return hashed.decode("utf-8")

    @staticmethod
    def create(username: str, email: str, plain_password: str):
        hash_password = users.generate_hash(plain_password)
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO users (username, email, hash_password) VALUES (%s, %s, %s)",
            (username, email, hash_password)
        )
        mysql.connection.commit()
        new_id = cur.lastrowid
        cur.close()
        return users(new_id, username, email, hash_password)

    @staticmethod
    def find_by_email(email: str):
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        row = cur.fetchone()
        cur.close()
        if row is None:
            return None
        return users(row["user_id"], row["username"], row["email"], row["hash_password"])

    @staticmethod
    def find_by_user_id(user_id: int):
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        row = cur.fetchone()
        cur.close()
        if row is None:
            return None
        return users(row["user_id"], row["username"], row["email"], row["hash_password"])

    