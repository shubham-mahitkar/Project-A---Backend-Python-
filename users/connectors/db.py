from users.app import app
# from flaskext.mysql import MySQL
from flask_mysqldb import MySQL

mysql = MySQL()
 
# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Shreyashmj95@'
app.config['MYSQL_DB'] = 'mysql'
mysql.init_app(app)

