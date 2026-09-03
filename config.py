import os
import MySQLdb.cursors
from dotenv import load_dotenv
load_dotenv()
 
class config:
   
    MYSQL_HOST = os.getenv('DB_HOST')
    MYSQL_USER = os.getenv('DB_USER')
    MYSQL_PASSWORD = os.getenv('DB_PASSWORD')
    MYSQL_DB = os.getenv('DB_NAME')
    SECRET_KEY = os.getenv('SECRET_KEY')
    MYSQL_CURSORCLASS = "DictCursor" 
    SECRET_KEY = os.getenv('SECRET_KEY')