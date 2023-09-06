from users.app import app
# from flaskext.mysql import MySQL
from flask_mysqldb import MySQL
import os


host = os.environ["HOST"]
user_name = os.environ["USER_NAME"]
user_password = os.environ["USER_PASSWORD"]
database = os.environ["USER_DB"]

mysql = MySQL()

# MySQL configurations
app.config['MYSQL_HOST'] = host
app.config['MYSQL_USER'] = user_name
app.config['MYSQL_PASSWORD'] = user_password
app.config['MYSQL_DB'] = database
mysql.init_app(app)

