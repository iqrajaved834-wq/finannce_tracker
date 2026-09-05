from flask import Flask,render_template
from utils.db import mysql
from utils.decorators import login_required
from config import config
from routes.user_routes import user_bp
from routes.transaction_routes import transaction_bp
from routes.category_routes import category_bp


app = Flask(__name__)
app.config.from_object(config)
mysql.init_app(app)


app.register_blueprint(user_bp)
app.register_blueprint(transaction_bp)
app.register_blueprint(category_bp)

@app.route("/")
def home():
    return render_template("login.html")


@app.route("/dashboard")
@login_required
def dashboard():
    
    return render_template("dashboard.html")


if __name__ == "__main__":
    app.run(debug=True)