import bcrypt
from utils.db import mysql

class users:
    #this function will be used to create a new object of user calss=> obj=user(id,username,email,password)
    def __init__(self,user_id,username,email,hash_password):
        self.user_id=user_id
        self.username=username
        self.email=email
        self.hash_password=hash_password

    #this function will be used to check whether  an entered [password and existing password are same...1=object password,2=entered password]
    def check_password(self, plain_password: str) -> bool:
         return bcrypt.checkpw(
            plain_password.encode("utf-8"),
            self.hash_password.encode("utf-8")
        )
    #this function is used to convert a plain passwordd int hash password by using bcrypt function 
    @staticmethod
    def hash_password(plain_password:str) -> str:
       salt=bcrypt.gensalt()
       hash= bcrypt.hashpw(
          plain_password.encode("utf-8"),
          salt
       )
       return hash.decode("utf-8")

    #this function is used to enter values,covery password into hash,save all infoermation into DB,get the id,and then creating a new object by passing values int user aboject
    @staticmethod
    def create(username:str,email:str,plain_password:str):
        hash_password=users.hash_password(plain_password)
        cur=mysql.connection.cursor()
        cur.execute(
           "insert into users(username,email,hash_password) values(%s,%s,%s)",
            (username,email,hash_password))
        mysql.connection.commit()    
        new_id=cur.lastrowid()
        cur.close()
        return users(new_id,username,email,hash_password)
    
     #this function will be used to fine user by email   
    @staticmethod
    def find_by_email(email:str):
        cur=mysql.connection.cursor()
        cur.execute(
            "select* from users where email=%s",(email,)
        )
        row=cur.fetchone()
        cur.close()
        if row is None:
            return None
        else:
            return {row["user_id"],row["username"],row["email"],row["hash_password"]}
        
    #this function is used to find user by id
    @staticmethod
    def find_by_user_id(user_id:int):
        cur=mysql.connection.cursor()
        cur.execute(
            "select* from users where user_id=%s",(user_id,)
             )
        row=cur.fetchone()
        cur.close()
        if row is None:
            return None
        else:
            return {row["user_id"],row["username"],row["email"],row["hash_password"]}

    #this function is used to show user data in the form of dictionary
    def to_dict(self):
        return {"user_id":self.id,"username":self.username,"email":self.email,"hash_password":self.hash_password}    

        
      