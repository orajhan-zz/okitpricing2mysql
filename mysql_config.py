from app import app
from flaskext.mysql import MySQL

mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'YourPassword'
app.config['MYSQL_DATABASE_DB'] = 'ociprice'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
