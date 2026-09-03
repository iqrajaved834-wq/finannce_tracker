from flask import Flask,request,jsonify,session
from config import  config
from utils.db import mysql
from models.user import users
from utils.decorators  import login_required
app=Flask(__name__)
app.config.from_object(config)
mysql.init_app(app)

@app.route('/')
def home():
    return"Finance tracker is live!!!"
@app.route('/test-db')
def test_db():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM categories")
        rows = cur.fetchall()
        cur.close()
        return {"status": "connected", "categories": rows}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.route('/signup',methods=['Post'])    
def signup():
     data=request.get_json()
     username=data.get('username')
     email=data.get('email')
     password=data.get('password')
     if not username or not email or not password:
          return jsonify({"error":"username,email,password all three are requires!"}),400
     if users.find_by_email(email) is not None:
          return jsonify({"error":"User already exist!you can try to login!"}),409

     user=users.create(username,email,password)
     return jsonify({"Message":"User added successfully","user":user.to_dict()}),201

@app.route("/login",methods=['Post'])
def login():
     data=request.get_json()
     email=data.get("email")
     password=data.get("password")
     if not email or not password:
          return jsonify({"error":"Email password both are required!!"}),400
     user=users.find_by_email(email) 
     if user is None or users.check_password(password) is False:
          return jsonify({"error": "Invalid email or password"}), 401
     if session['user_id']== user.user_id:
          return jsonify({"Message": "Login successfully!!!","user":user.to_dict()}),200
          
@app.route("/logout",methods=['Post']) 
def logout():
     session.pop('user_id',None)
     return jsonify({"Message": "Logout successfully!!!"}),200

@app.route('/profile',methods=['get'])
def profile():
     user=users.find_by_id()
     return jsonify({"Message": "Your profile  is here!!!","user":user.to_dict()}),200

if __name__=='__main__':
     app.run(debug=True)
