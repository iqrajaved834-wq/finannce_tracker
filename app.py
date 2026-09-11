from flask import Flask,render_template
from utils.db import mysql
from utils.decorators import login_required
from config import config
from routes.user_routes import user_bp
from routes.transaction_routes import transaction_bp
from routes.category_routes import category_bp
from routes.analytics_routes import analytics_bp
from routes.export_routes import export_bp


app = Flask(__name__)
app.config.from_object(config)
mysql.init_app(app)


app.register_blueprint(user_bp)
app.register_blueprint(transaction_bp)
app.register_blueprint(category_bp)
app.register_blueprint(analytics_bp)
app.register_blueprint(export_bp)

@app.route("/")
def home():
    return render_template("login.html")


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")

@app.route("/transactions-page")
@login_required
def transactions_page(): 
    return render_template("transactions.html")

@app.route("/categories-page")
@login_required
def category_page(): 
    return render_template("categories.html")

@app.route("/settings")
@login_required
def setting_page(): 
    return render_template("settings.html")

@app.route("/export-page")
@login_required
def export_page(): 
    return render_template("export.html")


if __name__ == "__main__":
    app.run(debug=True)