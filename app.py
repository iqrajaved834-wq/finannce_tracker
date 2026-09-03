from flask import Flask
from config import config
from utils.db import mysql
app = Flask(__name__)
app.config.from_object(config)
mysql.init_app(app)

@app.route('/')
def home():
    return "Finance Tracker is alive!"

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

if __name__ == '__main__':
    app.run(debug=True)