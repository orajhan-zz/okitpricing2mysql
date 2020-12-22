from app import app
from flaskext.mysql import MySQL

mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'AWSome123'
app.config['MYSQL_DATABASE_DB'] = 'ociprice'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

#docker run --privileged --restart always --name mysql8.0 -v /Users/jangwhan/mysql_data/8.0:/var/lib/mysql -p 3306:3306 -d -e MYSQL_ROOT_PASSWORD=AWSome123 mysql:8.0