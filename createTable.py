from flask import Flask

from dbconnect import connection

app = Flask(__name__)

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Its%yD8zx'
app.config['MYSQL_DATABASE_DB'] = 'Kaushik'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

conn, cursor = connection(app)

# conn = MySQLdb.connect(host="localhost",    # your host, usually localhost
#                        user="rahuldecoded",         # your username
#                        passwd="Rahul@95",  # your password
#                        db="Kaushik	") 


cursor.execute("DROP TABLE IF EXISTS Dishes")

sql = """CREATE TABLE Dishes ( 
		 dish_id INT(10) NOT NULL PRIMARY KEY AUTO_INCREMENT, 
		 dish_name VARCHAR(255) NOT NULL, 
		 dish_price FLOAT(10,2) NOT NULL, 
		 dish_url VARCHAR(255) NOT NULL, 
		 dish_type VARCHAR(20) NOT NULL, 
		 dish_desc VARCHAR(255) NOT NULL,
		 dish_nature VARCHAR(20) NOT NULL)"""

cursor.execute(sql)


# ------------------------------------------
cursor.execute("DROP TABLE IF EXISTS Orders")

sql = """CREATE TABLE Orders (
		 order_id INT(10) NOT NULL PRIMARY KEY AUTO_INCREMENT,
		 paymentMethod varchar(255) NOT NULL,
		 paymentStatus varchar(255) NOT NULL,
		 shippingAddress varchar(5) NOT NULL,
		 quantity INT(5) NOT NULL,
		 actualPrice FLOAT(10,2) NOT NULL,
		 discount FLOAT(2,2) DEFAULT 0,
		 diliveryAddress varchar(255) NOT NULL,
		 shipmentStatus varchar(10) NULL)"""		 

cursor.execute(sql)


# ------------------------------------------
cursor.execute("DROP TABLE IF EXISTS Cart")

sql = """CREATE TABLE Cart (
		 id INT(10) NOT NULL PRIMARY KEY AUTO_INCREMENT,
		 user_id varchar(30) NOT NULL,
		 item_ordered INT(10) NOT NULL,
		 quantity INT(5) NOT NULL,
		 odr_id INT(10) DEFAULT NULL,
		 FOREIGN KEY (item_ordered) REFERENCES Dishes(dish_id),
		 FOREIGN KEY (odr_id) REFERENCES Orders(order_id) ON UPDATE CASCADE)"""

cursor.execute(sql)


# ------------------------------
conn.close()

